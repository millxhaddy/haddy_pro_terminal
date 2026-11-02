"""
Diagnostik langsung sambungan Google Sheets dan barisan luar talian.
"""

import json
import os
import time
from urllib.error import URLError
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen

import pandas as pd
import streamlit as st

from dsr_engine import QUEUE_DIR
from engine_gsheets import (
    OFFICIAL_GSHEETS_TABS,
    get_configured_webhook_token,
    get_configured_webhook_url,
)


def _ping_webhook() -> dict:
    webhook_url = get_configured_webhook_url()
    if not webhook_url:
        return {"ok": False, "status": "NOT_CONFIGURED", "latency_ms": None}
    token = get_configured_webhook_token()
    if not token:
        return {"ok": False, "status": "TOKEN_NOT_CONFIGURED", "latency_ms": None}

    parts = urlsplit(webhook_url)
    if parts.scheme != "https" or parts.hostname != "script.google.com":
        return {"ok": False, "status": "INVALID_WEBHOOK_URL", "latency_ms": None}

    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query["action"] = "ping"
    query["token"] = token
    ping_url = urlunsplit(
        (parts.scheme, parts.netloc, parts.path, urlencode(query), "")
    )

    started_at = time.perf_counter()
    try:
        request = Request(
            ping_url,
            headers={"Accept": "application/json"},
            method="GET",
        )
        with urlopen(request, timeout=8) as response:
            payload = json.loads(response.read(65536).decode("utf-8"))
            latency_ms = round((time.perf_counter() - started_at) * 1000)
            if (
                response.status == 200
                and isinstance(payload, dict)
                and payload.get("status") == "ok"
            ):
                return {
                    "ok": True,
                    "status": "OK",
                    "latency_ms": latency_ms,
                }
            return {
                "ok": False,
                "status": "UNEXPECTED_RESPONSE",
                "latency_ms": latency_ms,
            }
    except (URLError, TimeoutError, OSError, ValueError):
        return {
            "ok": False,
            "status": "REQUEST_FAILED",
            "latency_ms": round((time.perf_counter() - started_at) * 1000),
        }


def get_system_health_metrics(vault: dict | None = None) -> dict:
    """Kira status daripada ping sebenar, metadata sync, dan barisan setempat."""
    ping = _ping_webhook()
    metadata = (vault or {}).get("_sync_metadata", {})
    tabs_total = len(OFFICIAL_GSHEETS_TABS)
    tabs_loaded = int(metadata.get("tabs_loaded", 0) or 0)
    source_tier = str(metadata.get("source_tier", "Belum diperiksa"))

    try:
        pending_count = sum(
            1
            for name in os.listdir(QUEUE_DIR)
            if name.startswith("pending_") and name.endswith(".json")
        )
    except OSError:
        pending_count = -1

    if ping["ok"] and tabs_loaded == tabs_total:
        overall_status = "🟢 Sambungan dan data aktif"
    elif ping["ok"] or tabs_loaded:
        overall_status = "🟡 Beroperasi sebahagian"
    else:
        overall_status = "🔴 Sambungan belum disahkan"

    latency = ping["latency_ms"]
    diagnostics = [
        {
            "Pemeriksaan": "Ping Google Apps Script",
            "Status": "🟢 OK" if ping["ok"] else f"🔴 {ping['status']}",
            "Butiran": f"{latency} ms" if latency is not None else "Tidak tersedia",
        },
        {
            "Pemeriksaan": "Tarikan tab Google Sheets",
            "Status": (
                "🟢 Lengkap"
                if tabs_loaded == tabs_total
                else "🟡 Sebahagian"
                if tabs_loaded
                else "⚪ Belum disahkan"
            ),
            "Butiran": f"{tabs_loaded}/{tabs_total} tab; {source_tier}",
        },
        {
            "Pemeriksaan": "Barisan transaksi luar talian",
            "Status": (
                "🔴 Tidak boleh dibaca"
                if pending_count < 0
                else "🟡 Menunggu penghantaran"
                if pending_count
                else "🟢 Kosong"
            ),
            "Butiran": (
                "Ralat membaca direktori"
                if pending_count < 0
                else f"{pending_count} transaksi menunggu"
            ),
        },
        {
            "Pemeriksaan": "Token webhook pada klien",
            "Status": (
                "🟢 Dikonfigurasi"
                if get_configured_webhook_token()
                else "🟡 Tiada"
            ),
            "Butiran": "Nilai rahsia tidak dipaparkan",
        },
    ]

    error_count = int(not ping["ok"]) + int(
        tabs_loaded != tabs_total or pending_count < 0
    )
    return {
        "table": pd.DataFrame(diagnostics),
        "summary": {
            "overall_status": overall_status,
            "active_feeds": (
                "1 configured webhook"
                if ping["status"]
                not in {
                    "NOT_CONFIGURED",
                    "INVALID_WEBHOOK_URL",
                    "TOKEN_NOT_CONFIGURED",
                }
                else "0 configured webhooks"
            ),
            "error_count": error_count,
            "avg_latency": (
                f"{latency} ms" if latency is not None else "Tidak tersedia"
            ),
            "uptime": "Belum diukur",
            "last_audit": time.strftime("%d-%m-%Y %H:%M:%S") + " MYT",
        },
    }


def render_system_diagnostics(vault: dict | None = None) -> None:
    health = get_system_health_metrics(vault)
    summary = health["summary"]

    st.subheader("🖥️ Diagnostik Langsung Google Sheets")
    status_col, ping_col, tabs_col, queue_col = st.columns(4)
    status_col.metric("Status", summary["overall_status"])
    ping_col.metric("Ping webhook", summary["avg_latency"])
    tabs_col.metric(
        "Tab diterima",
        str((vault or {}).get("_sync_metadata", {}).get("tabs_loaded", 0))
        + f"/{len(OFFICIAL_GSHEETS_TABS)}",
    )
    queue_col.metric(
        "Barisan luar talian",
        str(health["table"].iloc[2]["Butiran"]),
    )

    st.dataframe(
        health["table"],
        width="stretch",
        hide_index=True,
    )
    if not get_configured_webhook_token():
        st.warning(
            "Token webhook tiada pada klien. Tanpa HADDY_WEBHOOK_TOKEN yang sama "
            "di Script Properties dan Streamlit Secrets, endpoint mungkin boleh "
            "diakses tanpa pengesahan; jangan anggap konfigurasi ini gred bank."
        )
    source_tier = str(
        (vault or {}).get("_sync_metadata", {}).get("source_tier", "")
    )
    if "Tier-2 CSV" in source_tier:
        st.warning(
            "Sebahagian data dibaca melalui eksport CSV tanpa OAuth. Sahkan tetapan "
            "perkongsian spreadsheet sebelum menggunakan data kewangan sensitif."
        )
    st.caption(
        "Ping mengesahkan endpoint sahaja; bilangan tab mengesahkan data yang "
        "diterima. Uptime/SLA tidak dipaparkan kerana belum diukur."
    )
