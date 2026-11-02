"""
ENGINE GSHEETS v4.3 — HADDY PRO TERMINAL MILLX
Penyegerakan data 29 tab Google Sheets dengan fallback bertanda sumber:
  - Tier 1: Google Apps Script Web App Webhook (`doGet?action=get_all` & `doPost`)
  - Tier 2: Eksport CSV Gviz Langsung Google Sheets (Toleransi Baris Berbilang Jadual)
  - Tier 3: Cache Parquet Tempatan (`vault_parquet_cache/`) & Sandaran CSV Tempatan
"""
import os
import re
import io
import csv
import json
import glob
import urllib.request
from urllib.parse import quote
from datetime import datetime
import pandas as pd

try:
    import streamlit as st
except Exception:
    st = None

from dsr_engine import push_to_gsheets_webhook

# Direktori Cache Parquet Tempatan (Tier-3 Failover)
PARQUET_CACHE_DIR = os.path.join(os.getcwd(), "vault_parquet_cache")
os.makedirs(PARQUET_CACHE_DIR, exist_ok=True)

# 1. PEMETAAN RASMI 29 TAB HADDY PRO - TERMINAL MILLX
OFFICIAL_GSHEETS_TABS = {
    "pusat_kawalan": "00_Pusat Kawalan",
    "meja_keputusan": "01_Meja Keputusan",
    "pegangan_semasa": "02_Pegangan Semasa",
    "jurnal_dagangan": "03_Jurnal Dagangan",
    "senarai_pantau": "04_Senarai Pantau",
    "kalkulator_3m": "05_Kalkulator 3M",
    "pangkalan_1000": "06_Pangkalan 1000",
    "lejar_liabiliti": "10_Lejar Liabiliti",
    "skor_kredit": "11_Skor Kredit",
    "program_akpk": "12_Program AKPK",
    "sewa_beli_kereta": "13_Sewa Beli Kereta",
    "pinjaman_cimb": "14_Pinjaman CIMB",
    "kad_kredit_rhb": "15_Kad Kredit RHB",
    "radar_makro": "31_Radar Makro",
    "sejarah_dana": "40_Sejarah Dana",
    "sejarah_padanan": "41_Sejarah Padanan",
    "pantauan_pasaran": "60_Pantauan Pasaran",
    "semua_saham": "61_Semua Saham",
    "terminal_saham": "62_Terminal Saham",
    "ringkasan_mudah": "63_Ringkasan Mudah",
    "sistem_ddnk": "64_Sistem DDNK",
    "sistem_dagangan_pro": "65_Sistem Dagangan Pro",
    "aliran_tunai": "66_Aliran Tunai",
    "moomoo_rekod": "67_Moomoo Rekod",
    "cache_fundamental": "70_Cache Fundamental",
    "cache_ohlcv": "71_Cache OHLCV",
    "cache_earnings": "72_Cache Earnings",
    "konfigurasi_sistem": "90_Konfigurasi Sistem",
    "kesihatan_sistem": "91_Kesihatan Sistem",
}

# Skema Baris Pengepala Jadual Utama (1-based index mengikut struktur sebenar Google Sheets)
TAB_HEADER_SCHEMAS = {
    "00_Pusat Kawalan": 5,
    "01_Meja Keputusan": 4,
    "02_Pegangan Semasa": 1,
    "03_Jurnal Dagangan": 2,
    "66_Aliran Tunai": 2,
    "04_Senarai Pantau": 1,
    "05_Kalkulator 3M": 1,
    "06_Pangkalan 1000": 7,
    "10_Lejar Liabiliti": 1,
    "11_Skor Kredit": 13,
    "12_Program AKPK": 1,
    "13_Sewa Beli Kereta": 1,
    "14_Pinjaman CIMB": 6,
    "15_Kad Kredit RHB": 8,
}

# ======================================================================================
# 2. UTILITI RESOLUSI KONFIGURASI & PEMBERSIHAN RALAT FORMULA
# ======================================================================================
def get_configured_webhook_url() -> str:
    """Mendapatkan URL Web App Google Apps Script daripada st.secrets, session_state, atau env."""
    if st is not None:
        try:
            if "gsheets_webhook_url" in st.session_state and st.session_state["gsheets_webhook_url"]:
                return str(st.session_state["gsheets_webhook_url"]).strip()
            if hasattr(st, "secrets"):
                for k in ("GSHEETS_WEBHOOK_URL", "GOOGLE_SHEETS_WEBHOOK_URL", "WEBHOOK_URL"):
                    val = st.secrets.get(k, "")
                    if val:
                        return str(val).strip()
        except Exception:
            pass
    return os.environ.get("GSHEETS_WEBHOOK_URL", "").strip()


def get_configured_sheet_url() -> str:
    """Mendapatkan URL hamparan Google Sheets daripada session_state, st.secrets, atau env."""
    if st is not None:
        try:
            if "gsheets_live_url" in st.session_state and st.session_state["gsheets_live_url"]:
                return str(st.session_state["gsheets_live_url"]).strip()
            if hasattr(st, "secrets"):
                for k in ("GSHEETS_URL", "SPREADSHEET_URL", "GOOGLE_SHEETS_URL"):
                    val = st.secrets.get(k, "")
                    if val:
                        return str(val).strip()
                connections = st.secrets.get("connections", {})
                gsheets_connection = (
                    connections.get("gsheets", {})
                    if hasattr(connections, "get")
                    else {}
                )
                spreadsheet_url = (
                    gsheets_connection.get("spreadsheet", "")
                    if hasattr(gsheets_connection, "get")
                    else ""
                )
                if spreadsheet_url:
                    return str(spreadsheet_url).strip()
        except Exception:
            pass
    return os.environ.get("GSHEETS_URL", "").strip()


def should_refresh_snapshot(
    *,
    force: bool,
    snapshot_exists: bool,
    url_changed: bool,
    auto_sync_enabled: bool,
    now_epoch: float,
    last_attempt_epoch: float,
    interval_sec: int,
) -> bool:
    """Decide whether a remote pull is due, with a 60-second minimum interval."""
    if force or not snapshot_exists or url_changed:
        return True
    return bool(
        auto_sync_enabled
        and now_epoch - last_attempt_epoch >= max(60, int(interval_sec))
    )


def get_configured_webhook_token() -> str:
    """Mendapatkan token keselamatan pilihan HADDY_WEBHOOK_TOKEN."""
    if st is not None and hasattr(st, "secrets"):
        try:
            token = st.secrets.get("HADDY_WEBHOOK_TOKEN", "")
            connections = st.secrets.get("connections", {})
            gsheets_connection = (
                connections.get("gsheets", {})
                if hasattr(connections, "get")
                else {}
            )
            token = token or (
                gsheets_connection.get("HADDY_WEBHOOK_TOKEN", "")
                if hasattr(gsheets_connection, "get")
                else ""
            )
            if token:
                return str(token).strip()
        except Exception:
            pass
    return os.environ.get("HADDY_WEBHOOK_TOKEN", "").strip()


def is_public_csv_fallback_enabled() -> bool:
    """Public CSV is disabled unless explicitly enabled in Secrets or the environment."""
    value = False
    if st is not None and hasattr(st, "secrets"):
        try:
            value = st.secrets.get("GSHEETS_ALLOW_PUBLIC_CSV_FALLBACK", False)
        except Exception:
            value = False
    if not value:
        value = os.environ.get("GSHEETS_ALLOW_PUBLIC_CSV_FALLBACK", "")
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def heal_dataframe_errors(df: pd.DataFrame) -> pd.DataFrame:
    """Preserve spreadsheet formula errors so downstream views cannot mistake estimates for facts."""
    if not isinstance(df, pd.DataFrame) or df.empty:
        return df
    return df.copy()


def deduplicate_columns(headers: list) -> list:
    """Memastikan tiada nama lajur kosong atau pendua dalam DataFrame."""
    seen = {}
    result = []
    for idx, h in enumerate(headers):
        clean_h = str(h).strip()
        if not clean_h:
            clean_h = f"Col_{idx+1}"
        if clean_h in seen:
            seen[clean_h] += 1
            clean_h = f"{clean_h}_{seen[clean_h]}"
        else:
            seen[clean_h] = 1
        result.append(clean_h)
    return result


def rows_to_dataframe(rows: list, header_row_1based: int = 1, max_rows: int = None) -> pd.DataFrame:
    """
    Menukar senarai baris 2D (daripada Webhook JSON atau CSV berbilang lajur) kepada DataFrame
    tanpa ralat ParserError walaupun baris atas mempunyai bilangan lajur berbeza.
    """
    if not rows or len(rows) < header_row_1based:
        return pd.DataFrame()

    raw_headers = rows[header_row_1based - 1]
    last_valid_idx = len(raw_headers)
    while last_valid_idx > 0 and str(raw_headers[last_valid_idx - 1]).strip() == "":
        last_valid_idx -= 1
    if last_valid_idx == 0:
        last_valid_idx = len(raw_headers)

    headers = deduplicate_columns(raw_headers[:last_valid_idx])
    data_slice = rows[header_row_1based:]
    if max_rows is not None:
        data_slice = data_slice[:max_rows]

    normalized_rows = []
    for r in data_slice:
        if not any(str(cell).strip() != "" for cell in r):
            continue
        padded = list(r[:last_valid_idx]) + [""] * max(0, last_valid_idx - len(r))
        normalized_rows.append(padded)

    if not normalized_rows:
        return pd.DataFrame(columns=headers)

    df = pd.DataFrame(normalized_rows, columns=headers)
    return heal_dataframe_errors(df)


# ======================================================================================
# 3. PENGEKSTRAK SUB-JADUAL PINTAR MENGIKUT SPESIFIKASI TAB HADDY PRO
# ======================================================================================
def parse_specialized_tab_structures(tab_name: str, rows: list, vault: dict):
    """Mengekstrak sub-jadual khusus daripada tab berbilang seksyen."""
    if not rows:
        return

    if tab_name == "00_Pusat Kawalan":
        vault["direktori_roh_ai"] = rows_to_dataframe(rows, header_row_1based=5, max_rows=23)

    elif tab_name == "01_Meja Keputusan":
        bursa_hdr_idx = None
        us_hdr_idx = None
        for idx, r in enumerate(rows, start=1):
            joined = " ".join(str(c) for c in r)
            joined_lower = joined.lower()
            has_ticker_col = any(
                str(c).strip().lower() in {"ticker", "simbol", "kod", "stock"}
                for c in r
            )
            if not has_ticker_col:
                continue

            if "rm" in joined_lower or "bursa" in joined_lower or (bursa_hdr_idx is None and "usd" not in joined_lower):
                if bursa_hdr_idx is None:
                    bursa_hdr_idx = idx
            elif "usd" in joined_lower or us_hdr_idx is None:
                us_hdr_idx = idx

        if bursa_hdr_idx:
            df_b = rows_to_dataframe(rows, header_row_1based=bursa_hdr_idx, max_rows=15)
            if not df_b.empty:
                first_col = df_b.iloc[:, 0].astype(str).str.strip().str.rstrip(".")
                if first_col.str.isdigit().any():
                    df_b = df_b[first_col.str.isdigit()]
                vault["top10_bursa"] = df_b.head(10)
                vault["bursa_top10"] = df_b.head(10)

        if us_hdr_idx:
            df_u = rows_to_dataframe(rows, header_row_1based=us_hdr_idx, max_rows=15)
            if not df_u.empty:
                first_col_u = df_u.iloc[:, 0].astype(str).str.strip().str.rstrip(".")
                if first_col_u.str.isdigit().any():
                    df_u = df_u[first_col_u.str.isdigit()]
                vault["top10_us"] = df_u.head(10)
                vault["us_top10"] = df_u.head(10)

    elif tab_name == "03_Jurnal Dagangan":
        journal_header_idx = next(
            (
                idx
                for idx, row in enumerate(rows, start=1)
                if any("tarikh" in str(cell).lower() for cell in row)
                and any("ticker" in str(cell).lower() for cell in row)
            ),
            None,
        )
        if journal_header_idx:
            df_j = rows_to_dataframe(rows, header_row_1based=journal_header_idx)
            vault["jurnal_dagangan_df"] = df_j
            vault["trades_history"] = df_j

    elif tab_name == "02_Pegangan Semasa":
        holdings_header_idx = next(
            (
                idx
                for idx, row in enumerate(rows, start=1)
                if any("ticker" in str(cell).lower() or "simbol" in str(cell).lower() for cell in row)
                and any("kuantiti" in str(cell).lower() or "unit" in str(cell).lower() for cell in row)
            ),
            None,
        )
        if holdings_header_idx:
            vault["active_holdings_raw_df"] = rows_to_dataframe(
                rows, header_row_1based=holdings_header_idx
            )

    elif tab_name == "06_Pangkalan 1000":
        df_1k = rows_to_dataframe(rows, header_row_1based=7)
        vault["screener_1000"] = df_1k
        vault["df_1000"] = df_1k

    elif tab_name == "10_Lejar Liabiliti":
        df_ccris = rows_to_dataframe(rows, header_row_1based=1, max_rows=6)
        vault["ccris_facilities"] = df_ccris
        for idx, r in enumerate(rows, start=1):
            if any("Bulan Ke" in str(c) for c in r):
                vault["car_amortization_schedule"] = rows_to_dataframe(rows, header_row_1based=idx)
                break

    elif tab_name == "11_Skor Kredit":
        vault["iscore_bands"] = rows_to_dataframe(rows, header_row_1based=1, max_rows=5)
        for idx, r in enumerate(rows, start=1):
            if any("Parameter / Metrik" in str(c) for c in r):
                vault["dsr_credit_metrics"] = rows_to_dataframe(rows, header_row_1based=idx, max_rows=6)
                break

    elif tab_name == "12_Program AKPK":
        vault["akpk_payment_receipts"] = rows_to_dataframe(rows, header_row_1based=1, max_rows=1)
        for idx, r in enumerate(rows, start=1):
            if any(str(c).strip() == "Fasa" for c in r):
                vault["akpk_dmp_phases"] = rows_to_dataframe(rows, header_row_1based=idx, max_rows=22)
            elif any("Institusi Kewangan" in str(c) for c in r):
                vault["akpk_dmp_facilities"] = rows_to_dataframe(rows, header_row_1based=idx, max_rows=4)


# ======================================================================================
# 4. TIER-1, TIER-2 & TIER-3 DATA FETCHERS
# ======================================================================================
def fetch_all_tabs_via_webhook(webhook_url: str, timeout: int = 15) -> dict:
    """TIER 1: Menarik kesemua 29 tab serentak daripada Google Apps Script Web App (`?action=get_all`)."""
    if not webhook_url or not webhook_url.startswith("http"):
        return {"_fetch_metadata": {"request_ok": False, "error": "webhook_not_configured"}}

    token = get_configured_webhook_token()
    if not token:
        return {"_fetch_metadata": {"request_ok": False, "error": "webhook_token_not_configured"}}
    sep = "&" if "?" in webhook_url else "?"
    url = f"{webhook_url}{sep}action=get_all"
    url += f"&token={quote(token, safe='')}"

    vault = {}
    request_ok = False
    request_error = ""
    failed_tabs = []
    missing_tabs = []
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"}, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw_body = resp.read().decode("utf-8", errors="replace")
            payload = json.loads(raw_body)
            if not isinstance(payload, dict):
                request_error = "invalid_webhook_response"
            elif payload.get("status") == "ok" and isinstance(payload.get("vault"), dict):
                vault = payload["vault"]
                request_ok = True
                failed_tabs = payload.get("failed_tabs", [])
                missing_tabs = payload.get("missing_tabs", [])
            else:
                request_error = str(payload.get("code") or "invalid_webhook_response")
                failed_tabs = payload.get("failed_tabs", [])
                missing_tabs = payload.get("missing_tabs", [])
    except Exception as exc:
        request_error = type(exc).__name__

    def safe_tab_names(tab_names):
        if not isinstance(tab_names, list):
            return []
        known_tabs = set(OFFICIAL_GSHEETS_TABS.values())
        return [
            tab.strip()[:100]
            for tab in tab_names
            if isinstance(tab, str) and tab.strip() in known_tabs
        ][:len(OFFICIAL_GSHEETS_TABS)]

    failed_tabs = safe_tab_names(failed_tabs)
    missing_tabs = safe_tab_names(missing_tabs)
    received_tabs = sum(tab in vault for tab in OFFICIAL_GSHEETS_TABS.values())
    vault["_fetch_metadata"] = {
        "request_ok": request_ok,
        "request_count": 1,
        "tabs_received": received_tabs,
        "tabs_recovered": 0,
        "failed_tabs": failed_tabs,
        "missing_tabs": missing_tabs,
        "error": request_error,
        "fetch_mode": "get_all",
    }
    return vault


def fetch_tab_via_direct_csv(sheet_url: str, tab_name: str, timeout: int = 10) -> list:
    """TIER 2: Menarik baris 2D lembaran secara terus melalui titik akhir gviz CSV Google Sheets."""
    if not sheet_url or not is_public_csv_fallback_enabled():
        return []
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", str(sheet_url))
    if not match:
        return []
    doc_key = match.group(1)
    csv_url = f"https://docs.google.com/spreadsheets/d/{doc_key}/gviz/tq?tqx=out:csv&sheet={quote(tab_name)}"
    try:
        req = urllib.request.Request(csv_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            text_data = resp.read().decode("utf-8", errors="replace")
            return list(csv.reader(io.StringIO(text_data)))
    except Exception:
        return []


def save_df_to_parquet_cache(tab_name: str, df: pd.DataFrame):
    """Menyimpan DataFrame yang berjaya disegerakkan ke dalam storan Parquet tempatan (Tier 3)."""
    if not isinstance(df, pd.DataFrame) or df.empty:
        return
    safe_name = re.sub(r"[^a-zA-Z0-9_]", "_", tab_name)
    fpath = os.path.join(PARQUET_CACHE_DIR, f"{safe_name}.parquet")
    try:
        df_str = df.astype(str)
        df_str.to_parquet(fpath, index=False)
    except Exception:
        csv_fallback = os.path.join(PARQUET_CACHE_DIR, f"{safe_name}.csv")
        try:
            df.to_csv(csv_fallback, index=False, encoding="utf-8")
        except Exception:
            pass


def load_local_fallback_rows(tab_name: str) -> list:
    """TIER 3: Membaca daripada fail CSV eksport tempatan atau cache tempatan jika luar talian."""
    safe_suffix = tab_name.replace(" ", "_")
    parquet_path = os.path.join(
        PARQUET_CACHE_DIR,
        f"{re.sub(r'[^a-zA-Z0-9_]', '_', tab_name)}.parquet",
    )
    if os.path.exists(parquet_path):
        try:
            cached_df = pd.read_parquet(parquet_path)
            if not cached_df.empty:
                header_row = TAB_HEADER_SCHEMAS.get(tab_name, 1)
                rows = [[] for _ in range(header_row - 1)]
                rows.append([str(column) for column in cached_df.columns])
                rows.extend(cached_df.fillna("").astype(str).values.tolist())
                return rows
        except Exception:
            pass

    candidates = [
        f"Haddy_Pro_Terminal_Millx_{safe_suffix}.csv",
        f"{safe_suffix}.csv",
        os.path.join(PARQUET_CACHE_DIR, f"{ re.sub(r'[^a-zA-Z0-9_]', '_', tab_name) }.csv"),
    ]
    for cand in candidates:
        if os.path.exists(cand):
            try:
                with open(cand, "r", encoding="utf-8", errors="replace") as fp:
                    return list(csv.reader(fp))
            except Exception:
                pass

    prefix_num = tab_name.split("_")[0] if "_" in tab_name else ""
    if prefix_num.isdigit():
        matched = glob.glob(f"*{prefix_num}_*.csv")
        if matched:
            try:
                with open(matched[0], "r", encoding="utf-8", errors="replace") as fp:
                    return list(csv.reader(fp))
            except Exception:
                pass
    return []


# ======================================================================================
# 5. FUNGSI UTAMA: load_all_terminal_data() & HELPER 2-WAY PUSH
# ======================================================================================
def load_all_terminal_data() -> dict:
    """
    Memuatkan kesemua 29 tab rasmi Haddy Pro - Terminal Millx secara automatik:
      1. Cuba Tier 1 (Google Apps Script Web App `doGet?action=get_all`)
      2. Cuba Tier 2 (Direct Google Sheets CSV Export)
      3. Cuba Tier 3 (Local CSV / Parquet Cache Failover)
    """
    webhook_url = get_configured_webhook_url()
    sheet_url = get_configured_sheet_url()

    vault = {
        "_sync_metadata": {
            "timestamp": "",
            "source_tier": "Tier-3 Local Cache",
            "tabs_loaded": 0,
            "remote_verified": False,
        }
    }

    webhook_tabs_raw = fetch_all_tabs_via_webhook(webhook_url)
    fetch_mode = webhook_tabs_raw.pop("_fetch_mode", "")
    webhook_metadata = webhook_tabs_raw.pop(
        "_fetch_metadata",
        {"request_ok": False, "request_count": 0, "tabs_recovered": 0, "error": ""},
    )

    loaded_count = 0
    webhook_tab_count = sum(
        tab_title in webhook_tabs_raw for tab_title in OFFICIAL_GSHEETS_TABS.values()
    )
    used_direct_csv = False
    used_local_cache = False
    tab_sources = {}
    tab_cache_timestamps = {}
    for alias, tab_title in OFFICIAL_GSHEETS_TABS.items():
        rows = webhook_tabs_raw.get(tab_title, [])
        tab_source = "webhook" if rows else ""

        if not rows and sheet_url:
            rows = fetch_tab_via_direct_csv(sheet_url, tab_title)
            used_direct_csv = used_direct_csv or bool(rows)
            if rows:
                tab_source = "direct Google Sheets CSV"

        if not rows:
            rows = load_local_fallback_rows(tab_title)
            used_local_cache = used_local_cache or bool(rows)
            if rows:
                tab_source = "local cache"
                safe_name = re.sub(r"[^a-zA-Z0-9_]", "_", tab_title)
                cache_path = os.path.join(PARQUET_CACHE_DIR, f"{safe_name}.parquet")
                if os.path.exists(cache_path):
                    tab_cache_timestamps[alias] = datetime.fromtimestamp(
                        os.path.getmtime(cache_path)
                    ).isoformat(timespec="seconds")

        header_row = TAB_HEADER_SCHEMAS.get(tab_title, 1)
        df_tab = rows_to_dataframe(rows, header_row_1based=header_row)
        tab_sources[alias] = tab_source or "unavailable"

        if not df_tab.empty:
            loaded_count += 1
            if tab_source != "local cache":
                save_df_to_parquet_cache(tab_title, df_tab)

        vault[tab_title] = df_tab
        vault[alias] = df_tab
        vault[f"_raw_rows_{alias}"] = rows

        parse_specialized_tab_structures(tab_title, rows, vault)

    vault["_sync_metadata"]["tabs_loaded"] = loaded_count
    vault["_sync_metadata"]["tab_sources"] = tab_sources
    vault["_sync_metadata"]["tab_cache_timestamps"] = tab_cache_timestamps
    if webhook_metadata.get("request_ok"):
        source_tier = (
            "Tier-1 Webhook Live (per-tab recovery)"
            if fetch_mode == "per_tab_fallback"
            else "Tier-1 Webhook Live"
        )
        if used_direct_csv:
            source_tier += " + Tier-2 CSV fallback"
        if used_local_cache:
            source_tier += " + Tier-3 local fallback"
    elif used_direct_csv:
        source_tier = "Tier-2 Direct GSheets Live"
        if used_local_cache:
            source_tier += " + Tier-3 local fallback"
    elif used_local_cache:
        source_tier = "Tier-3 Local Cache"
    else:
        source_tier = "No data source available"
    remote_verified = bool(webhook_metadata.get("request_ok") or used_direct_csv)
    received_webhook_tabs = int(
        webhook_metadata.get("tabs_received", webhook_tab_count) or 0
    )
    remote_data_confirmed = bool(used_direct_csv or received_webhook_tabs)
    vault["_sync_metadata"]["source_tier"] = source_tier
    vault["_sync_metadata"]["remote_verified"] = remote_verified
    vault["_sync_metadata"]["webhook_request_count"] = int(
        webhook_metadata.get("request_count", 0) or 0
    )
    vault["_sync_metadata"]["webhook_tabs_received"] = received_webhook_tabs
    vault["_sync_metadata"]["remote_data_confirmed"] = remote_data_confirmed
    vault["_sync_metadata"]["webhook_tabs_recovered"] = int(
        webhook_metadata.get("tabs_recovered", 0) or 0
    )
    vault["_sync_metadata"]["remote_failed_tabs"] = webhook_metadata.get(
        "failed_tabs", []
    )
    vault["_sync_metadata"]["remote_missing_tabs"] = webhook_metadata.get(
        "missing_tabs", []
    )
    vault["_sync_metadata"]["cached_tabs"] = sum(
        source == "local cache" for source in tab_sources.values()
    )
    vault["_sync_metadata"]["remote_error"] = str(webhook_metadata.get("error", ""))
    vault["_sync_metadata"]["data_freshness"] = (
        "remote" if remote_data_confirmed else (
            "remote_response_no_tabs" if remote_verified else
            "local_cache" if used_local_cache else "unavailable"
        )
    )
    if remote_verified and not remote_data_confirmed:
        vault["_sync_metadata"]["remote_error"] = "no_recognized_tabs_returned"
    attempt_timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    vault["_sync_metadata"]["attempt_timestamp"] = attempt_timestamp
    vault["_sync_metadata"]["timestamp"] = (
        attempt_timestamp if remote_data_confirmed else None
    )
    return vault


def push_row_to_gsheets(tab_name: str, row_data, action: str = "upsert_row", key_value: str = None) -> bool:
    """Menolak (Push) baris baharu atau mengemas kini baris sedia ada melalui Web App `doPost`."""
    webhook_url = get_configured_webhook_url()
    token = get_configured_webhook_token()
    payload = {
        "action": action,
        "tab": tab_name,
        "data": row_data,
        "timestamp": datetime.now().isoformat(),
    }
    if key_value is not None:
        payload["key_value"] = str(key_value)
    if token:
        payload["token"] = token

    return push_to_gsheets_webhook(webhook_url, payload)


def push_3m_calculator_to_gsheets(
    ticker: str,
    max_risk_rm: float,
    entry_price: float,
    stop_loss: float,
    take_profit: float,
    market_type: str = "Bursa Malaysia (100 unit/lot)",
    gross_capital: float = 10000.0,
) -> bool:
    """Mengemas kini parameter input Kalkulator 3M (`05_Kalkulator 3M`) secara terus di Google Sheets."""
    webhook_url = get_configured_webhook_url()
    token = get_configured_webhook_token()
    payload = {
        "action": "update_3m",
        "tab": "05_Kalkulator 3M",
        "ticker": ticker,
        "max_risk_rm": max_risk_rm,
        "entry_price": entry_price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "market_type": market_type,
        "gross_capital": gross_capital,
        "timestamp": datetime.now().isoformat(),
    }
    if token:
        payload["token"] = token

    return push_to_gsheets_webhook(webhook_url, payload)