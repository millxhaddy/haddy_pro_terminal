"""
DSR ENGINE (DYNAMIC SYSTEM RESILIENCE) v4.3 - GRED TENTERA & PERBANKAN
Enjin Penyegerakan 2-Hala (Streamlit ⟷ Google Sheets Webhook) & Barisan Luar Talian (Offline Queue)
Dipadankan khusus dengan 29 Tab Rasmi Haddy Pro - Terminal Millx
"""
import os
import json
import tempfile
import uuid
import urllib.request
from datetime import datetime

QUEUE_DIR = os.path.join(os.getcwd(), "dsr_offline_queue")
os.makedirs(QUEUE_DIR, exist_ok=True)


def enqueue_offline_payload(payload: dict) -> str:
    """Simpan transaksi tanpa kredensial dalam barisan luar talian secara atomik."""
    os.makedirs(QUEUE_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    tab_name = payload.get("tab")
    if tab_name:
        safe_tab_name = "".join(
            char if char.isalnum() or char in "-_" else "_"
            for char in str(tab_name)
        ).strip("_")
        prefix = f"{safe_tab_name}_" if safe_tab_name else ""
    else:
        prefix = ""
    fname = f"pending_{prefix}{ts}_{uuid.uuid4().hex[:6]}.json"
    fpath = os.path.join(QUEUE_DIR, fname)
    payload_with_meta = dict(payload)
    for credential_key in ("token", "api_key", "secret"):
        payload_with_meta.pop(credential_key, None)
    payload_with_meta.setdefault("queued_at", datetime.now().isoformat())
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=QUEUE_DIR,
            prefix=".pending_",
            suffix=".tmp",
            delete=False,
        ) as temp_file:
            temp_path = temp_file.name
            json.dump(payload_with_meta, temp_file, ensure_ascii=False, indent=2)
            temp_file.flush()
            os.fsync(temp_file.fileno())
        os.replace(temp_path, fpath)
    except Exception:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        raise
    return fpath


def push_to_gsheets_webhook(webhook_url: str, payload: dict, timeout: int = 12) -> bool:
    """
    Menghantar muatan JSON ke Google Apps Script Web App (`doPost`).
    Jika gagal atau tiada URL webhook, muatan disimpan secara automatik ke dalam `QUEUE_DIR`.
    """
    if (
        not webhook_url
        or not str(webhook_url).strip().startswith("https://")
        or not payload.get("token")
    ):
        enqueue_offline_payload(payload)
        return False

    try:
        data_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            str(webhook_url).strip(),
            data=data_bytes,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            res_json = json.loads(body)
            if not isinstance(res_json, dict):
                raise ValueError("Google Apps Script returned a non-object response")
            result = res_json.get("result")
            if (
                res_json.get("status") == "ok"
                and isinstance(result, dict)
                and result.get("status")
                in {"appended", "inserted", "updated", "updated_3m", "cells_updated"}
            ):
                return True
    except Exception:
        pass

    enqueue_offline_payload(payload)
    return False


def write_transaction_with_dsr(
    tab_name: str,
    row_data: dict,
    webhook_url: str = "",
    timeout: int = 12,
    action: str = "upsert_row",
    token: str = "",
) -> dict:
    """Hantar baris ke webhook; gilirkannya secara setempat jika penghantaran gagal."""
    payload = {
        "action": action,
        "tab": tab_name,
        "data": dict(row_data),
        "timestamp": datetime.now().isoformat(),
    }
    if token:
        payload["token"] = token
    synced = push_to_gsheets_webhook(webhook_url, payload, timeout=timeout)
    return {
        "status": "SYNCED" if synced else "QUEUED",
        "tab": tab_name,
    }


def sync_queued_inputs(webhook_url: str = "", timeout: int = 15, token: str = "") -> int:
    """
    Menyegerakkan semula semua fail `pending_*.json` di dalam `QUEUE_DIR` ke Google Sheets
    menggunakan panggilan kelompok (`action: "batch_sync"`) sebaik sahaja sambungan pulih.
    """
    if not os.path.exists(QUEUE_DIR):
        return 0

    pending_files = sorted(
        [
            os.path.join(QUEUE_DIR, f)
            for f in os.listdir(QUEUE_DIR)
            if f.startswith("pending_") and f.endswith(".json")
        ]
    )
    if (
        not pending_files
        or not webhook_url
        or not str(webhook_url).strip().startswith("https://")
        or not token
    ):
        return 0

    items = []
    valid_files = []
    for fpath in pending_files:
        try:
            with open(fpath, "r", encoding="utf-8") as fp:
                item = json.load(fp)
                if not isinstance(item, dict):
                    continue
                for credential_key in ("token", "api_key", "secret"):
                    item.pop(credential_key, None)
                items.append(item)
                valid_files.append(fpath)
        except Exception:
            pass

    if not items:
        return 0

    batch_payload = {
        "action": "batch_sync",
        "items": items,
        "synced_from": "Haddy_Pro_Streamlit_v4.3",
        "timestamp": datetime.now().isoformat(),
    }
    if token:
        batch_payload["token"] = token

    try:
        data_bytes = json.dumps(batch_payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            str(webhook_url).strip(),
            data=data_bytes,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            res_json = json.loads(body)
            if not isinstance(res_json, dict):
                raise ValueError("Google Apps Script returned a non-object response")
            results = res_json.get("results")
            if (
                res_json.get("status") == "ok"
                and isinstance(results, list)
                and len(results) == len(valid_files)
            ):
                synced_count = 0
                for fpath, result in zip(valid_files, results):
                    if not isinstance(result, dict) or result.get("status") not in {
                        "appended",
                        "inserted",
                        "updated",
                        "updated_3m",
                        "cells_updated",
                    }:
                        continue
                    try:
                        os.remove(fpath)
                        synced_count += 1
                    except OSError:
                        continue
                return synced_count
    except Exception:
        return 0

    return 0
