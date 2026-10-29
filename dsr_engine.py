"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL TERAS: DYNAMIC SYSTEM RESILIENCE (DSR) & PENYEGERAKAN 2-HALA
1. Auto-Failover (Multi-Source Georedundancy)
2. Local Replica Caching (Parquet / JSON Local Engine)
3. Input Queueing (Zero-Loss Offline Write Buffer)
4. Self-Healing Automatic Sync-Back
========================================================================================
"""

import os
import json
import time
import pandas as pd
import urllib.request
import urllib.parse
from datetime import datetime

CACHE_DIR = ".dsr_cache"
QUEUE_DIR = ".dsr_queue"

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(QUEUE_DIR, exist_ok=True)

DOC_ID = "1lyA9GEChz07i_9X_keem9TJJ2XHMMNaIEzFrqbQ3QAI"

# --------------------------------------------------------------------------------------
# 1. ENJIN BACAAN DSR (FAILOVER DINAMIK 3-PERINGKAT)
# --------------------------------------------------------------------------------------
def fetch_sheet_with_dsr(tab_name: str, gid: int, header_row: int = 0, max_retries: int = 2) -> tuple:
    """
    Menyedut data Google Sheets dengan perlindungan DSR:
    Tier 1: Google Sheets CSV Direct Stream
    Tier 2: Google Visualization API Fallback (gviz/tq)
    Tier 3: Local Replica Cache (Parquet/JSON) - Menjamin UI tidak terhenti jika Google offline/429
    """
    clean_tab = str(tab_name).replace(" ", "_")
    parquet_path = os.path.join(CACHE_DIR, f"{clean_tab}_{gid}.parquet")
    json_path = os.path.join(CACHE_DIR, f"{clean_tab}_{gid}.json")
    
    csv_url = f"https://docs.google.com/spreadsheets/d/{DOC_ID}/export?format=csv&gid={gid}"
    
    # Percubaan Tier 1: CSV Direct Export
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(csv_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=4) as resp:
                df = pd.read_csv(resp, skiprows=header_row, on_bad_lines="skip")
                
            if df is not None and not df.empty:
                df = df.dropna(how="all")
                df = df.loc[:, ~df.columns.astype(str).str.contains('^Unnamed', na=False)]
                df.columns = [str(col).strip() for col in df.columns]
                
                # Simpan salinan replika tempatan serta-merta (Disaster Recovery Copy)
                try:
                    df.to_parquet(parquet_path, index=False)
                except Exception:
                    df.to_json(json_path, orient="records")
                    
                return df, "🟢 LIVE (PRIMARY GOOGLE CLOUD CORE)"
        except Exception:
            time.sleep(0.3 * attempt)
            
    # Percubaan Tier 2: Google Visualization API Fallback
    try:
        encoded_name = urllib.parse.quote(tab_name)
        gviz_url = f"https://docs.google.com/spreadsheets/d/{DOC_ID}/gviz/tq?tqx=out:csv&sheet={encoded_name}"
        req_gviz = urllib.request.Request(gviz_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req_gviz, timeout=4) as resp_gviz:
            df_gviz = pd.read_csv(resp_gviz, skiprows=header_row, on_bad_lines="skip")
        if df_gviz is not None and not df_gviz.empty:
            df_gviz = df_gviz.dropna(how="all")
            df_gviz = df_gviz.loc[:, ~df_gviz.columns.astype(str).str.contains('^Unnamed', na=False)]
            df_gviz.columns = [str(col).strip() for col in df_gviz.columns]
            try:
                df_gviz.to_parquet(parquet_path, index=False)
            except Exception:
                df_gviz.to_json(json_path, orient="records")
            return df_gviz, "🟡 DSR TIER 2 (GVIZ FAILOVER ACTIVE)"
    except Exception:
        pass

    # Percubaan Tier 3: Peralihan ke Replika Tempatan (Local Parquet / JSON Cache)
    if os.path.exists(parquet_path):
        try:
            df_local = pd.read_parquet(parquet_path)
            return df_local, "🛡️ DSR TIER 3: LOCAL PARQUET REPLICA (OFFLINE ZERO-DOWNTIME)"
        except Exception:
            pass

    if os.path.exists(json_path):
        try:
            df_local_json = pd.read_json(json_path)
            return df_local_json, "🛡️ DSR TIER 3: LOCAL JSON REPLICA (OFFLINE ZERO-DOWNTIME)"
        except Exception:
            pass

    return pd.DataFrame(), "🔴 DSR CRITICAL: NO SOURCE REACHABLE"


# --------------------------------------------------------------------------------------
# 2. ENJIN PENULISAN 2-HALA & INPUT QUEUEING (PENCEGAH HILANG REKOD)
# --------------------------------------------------------------------------------------
def write_transaction_with_dsr(tab_name: str, payload_data: dict, webhook_url: str = "") -> dict:
    """
    Menulis transaksi dengan jaminan DSR:
    Jika Webhook dalam talian -> Tulis terus ke Google Sheets.
    Jika luar talian/ralat kuota -> Simpan ke baris gilir (.dsr_queue) tanpa kehilangan data.
    """
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    queue_file = os.path.join(QUEUE_DIR, f"pending_{tab_name}_{now_str}.json")

    # 1. Cuba hantar terus jika webhook tersedia
    if webhook_url:
        try:
            req_data = json.dumps({
                "target_sheet": tab_name,
                "action": "append_row",
                "data": payload_data
            }).encode("utf-8")
            
            req = urllib.request.Request(webhook_url, data=req_data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=4) as response:
                if response.status == 200:
                    return {
                        "status": "SUCCESS",
                        "mode": "2-WAY LIVE WRITE",
                        "msg": "Data berjaya dimasukkan ke Google Sheets secara langsung!"
                    }
        except Exception:
            pass  # Beralih secara autonomi ke Baris Gilir Luar Talian

    # 2. Masukkan ke Baris Gilir Tempatan (Input Queueing)
    with open(queue_file, "w", encoding="utf-8") as f:
        json.dump({"tab": tab_name, "data": payload_data, "time": now_str}, f, ensure_ascii=False, indent=2)

    return {
        "status": "QUEUED",
        "mode": "DSR INPUT QUEUE",
        "msg": "Sambungan Google Sheets terganggu. Data disimpan rapi dalam Teras Baris Gilir Tempatan (.dsr_queue) dan akan disegerakkan secara automatik apabila talian pulih."
    }


# --------------------------------------------------------------------------------------
# 3. PENYEGERAKAN SEMULA AUTOMATIK (SELF-HEALING SYNC-BACK)
# --------------------------------------------------------------------------------------
def sync_queued_inputs(webhook_url: str) -> int:
    """
    Menolak balik semua transaksi tertunggak ke Google Sheets apabila talian pulih.
    Mengembalikan bilangan fail yang berjaya disegerak.
    """
    if not webhook_url:
        return 0
        
    queue_files = [os.path.join(QUEUE_DIR, f) for f in os.listdir(QUEUE_DIR) if f.startswith("pending_") and f.endswith(".json")]
    synced_count = 0
    
    for qf in queue_files:
        try:
            with open(qf, "r", encoding="utf-8") as f:
                item = json.load(f)
            req_data = json.dumps({
                "target_sheet": item["tab"],
                "action": "append_row",
                "data": item["data"]
            }).encode("utf-8")
            
            req = urllib.request.Request(webhook_url, data=req_data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=4) as response:
                if response.status == 200:
                    os.remove(qf)
                    synced_count += 1
        except Exception:
            break
            
    return synced_count