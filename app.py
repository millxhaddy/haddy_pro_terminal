"""
HADDY PRO - Terminal Millx v4.3
Refresh Google Sheets berjadual dengan fallback cache yang dipaparkan secara berasingan.
"""
import os
import re
import sys
import time
import inspect
import logging
from urllib.parse import quote
import streamlit as st
import pandas as pd
from datetime import datetime
from dsr_engine import sync_queued_inputs, QUEUE_DIR


# ======================================================================================
# 0. PERISAI KESELAMATAN & AUTO-KEY WIDGET (MENCEGAH DUPLICATE ELEMENT ID)
# ======================================================================================
def install_streamlit_autokey_guard():
    st._haddy_callsite_counts = {}
    st._haddy_used_keys = set()
    target_widgets = [
        "text_input", "number_input", "text_area", "selectbox", "multiselect",
        "slider", "select_slider", "button", "checkbox", "radio", "toggle",
        "date_input", "time_input", "file_uploader", "color_picker",
        "plotly_chart", "data_editor", "chat_input", "audio_input",
        "pills", "segmented_control"
    ]

    def _wrap_widget_fn(orig_fn, w_name):
        try:
            sig = inspect.signature(orig_fn)
            has_key_param = "key" in sig.parameters or any(
                p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
            )
        except Exception:
            has_key_param = True

        if not has_key_param:
            return orig_fn

        def _wrapped(*args, **kwargs):
            caller_file, caller_line = "app", 0
            try:
                frame = sys._getframe(1)
                while frame is not None:
                    fname = os.path.basename(frame.f_code.co_filename)
                    if fname not in ("metrics_util.py",) and not frame.f_code.co_name.startswith("_wrapped"):
                        caller_file = os.path.splitext(fname)[0]
                        caller_line = frame.f_lineno
                        break
                    frame = frame.f_back
            except Exception:
                pass

            label_raw = str(args[0])[:20] if args else str(kwargs.get("label", ""))[:20]
            label_clean = "".join(ch if ch.isalnum() else "_" for ch in label_raw).strip("_") or "w"
            callsite_id = (w_name, caller_file, caller_line, label_clean)
            call_count = st._haddy_callsite_counts.get(callsite_id, 0) + 1
            st._haddy_callsite_counts[callsite_id] = call_count

            explicit_key = kwargs.get("key")
            candidate_key = (
                str(explicit_key)
                if explicit_key is not None
                else f"hk_{w_name}_{caller_file}_L{caller_line}_{label_clean}_{call_count}"
            )

            if candidate_key in st._haddy_used_keys:
                dup_idx = 2
                while f"{candidate_key}__dup{dup_idx}" in st._haddy_used_keys:
                    dup_idx += 1
                candidate_key = f"{candidate_key}__dup{dup_idx}"

            st._haddy_used_keys.add(candidate_key)
            kwargs["key"] = candidate_key
            return orig_fn(*args, **kwargs)

        return _wrapped

    try:
        from streamlit.delta_generator import DeltaGenerator
        for w_name in target_widgets:
            if hasattr(DeltaGenerator, w_name):
                orig_dg_attr = f"_haddy_orig_dg_{w_name}"
                if not hasattr(DeltaGenerator, orig_dg_attr):
                    setattr(DeltaGenerator, orig_dg_attr, getattr(DeltaGenerator, w_name))
                setattr(DeltaGenerator, w_name, _wrap_widget_fn(getattr(DeltaGenerator, orig_dg_attr), w_name))
                if hasattr(st, "_main") and hasattr(st._main, w_name):
                    setattr(st, w_name, getattr(st._main, w_name))
    except Exception:
        pass

    try:
        import streamlit.elements.lib.utils as st_elem_utils
        if hasattr(st_elem_utils, "_register_element_id"):
            if not hasattr(st_elem_utils, "_haddy_orig_register_element_id"):
                st_elem_utils._haddy_orig_register_element_id = st_elem_utils._register_element_id

            def _safe_register_element_id(ctx, element_type, element_id):
                try:
                    return st_elem_utils._haddy_orig_register_element_id(ctx, element_type, element_id)
                except Exception:
                    return None

            st_elem_utils._register_element_id = _safe_register_element_id
    except Exception:
        pass


install_streamlit_autokey_guard()

# 1. Konfigurasi Halaman & Kunci Keselamatan AES-256 Mandatori
from security_vault import verify_vault_authentication

st.set_page_config(
    page_title="Haddy Pro v4.3 - Terminal Millx",
    page_icon="haddy_logo.png" if os.path.exists("haddy_logo.png") else "🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

verify_vault_authentication()

# 2. Import Modul Bersepadu
from gold_master_release import render_gold_master_dashboard
from unusual_volume_anomaly import render_unusual_volume_scanner_ui
from portfolio_opt_debt_strategy import render_markowitz_efficient_frontier_ui, render_debt_payoff_strategies_ui
from fundamental_health_sankey import render_fundamental_health_and_sankey_ui
from chat_copilot_dcf import render_interactive_chat_copilot
from order_dialog_cost_engine import open_quick_order_modal
from engine_gsheets import (
    get_configured_sheet_url,
    get_configured_webhook_url,
    get_configured_webhook_token,
    is_public_csv_fallback_enabled,
    load_all_terminal_data,
    should_refresh_snapshot,
)
from pipeline_cleaner import process_master_database
from metrics_bento import extract_portfolio_kpis
from portfolio_risk_alerts import render_holding_risk_alerts
from portfolio_workspace import (
    render_journal_export,
    render_portfolio_data_status,
    render_portfolio_manager,
)
from visuals_cashflow import get_cashflow_dataframe, render_cumulative_equity_curve, render_annual_flow_breakdown
from portfolio_holdings import get_active_holdings, render_allocation_donut, render_holdings_cards
from decision_tables import get_top10_bursa, get_top10_us, render_rr_comparison_chart
from master_screener import build_institutional_screener_data, render_canslim_bubble_matrix
from risk_calculator_audio import render_3m_calculator_ui, AUDIO_SOUNDS
from moomoo_journal_analytics import render_moomoo_order_generator, render_journal_analytics_dashboard
from system_diagnostics import render_system_diagnostics
from trade_desk import render_trade_desk_ui
from postmortem_desk import render_postmortem_dashboard
from market_heatmap import render_market_heatmap_tab
from advanced_quant_suite import render_monte_carlo_ui, render_correlation_matrix_ui, render_earnings_dividend_hub
from ai_copilot_mentor import render_ai_copilot_ui
from million_milestone import render_milestone_tracker_ui
from zakat_compliance import render_zakat_compliance_ui
from report_exporter import render_report_exporter_ui
from trailing_sentinel import render_trailing_sentinel_ui
from backtest_engine import render_backtest_ui
from voice_assistant import render_voice_assistant_ui
from paper_autopilot import render_paper_autopilot_ui
from tax_ledger import render_tax_ledger_ui
from crisis_playbook import render_crisis_playbook_ui
from ai_cyborg_sentinel import render_robot_mindset_hud, render_traffic_light_evaluator
from hardcore_ai_engine import render_hardcore_ai_soul_hud
from debt_management_ui import render_debt_management_dashboard
from personal_finance_suite import render_personal_finance_suite
from fluent_core_engine import get_dual_market_status
from modern_grid_ui import render_modern_decision_grid
from macro_intelligence_hub import render_macro_intelligence_dashboard

logger = logging.getLogger(__name__)


def smart_invoke(func, **context):
    """Invoke a renderer with supported context and report failures visibly."""
    try:
        sig = inspect.signature(func)
        accepts_extra_kwargs = any(
            parameter.kind == inspect.Parameter.VAR_KEYWORD
            for parameter in sig.parameters.values()
        )
        kwargs = (
            context
            if accepts_extra_kwargs
            else {
                key: value
                for key, value in context.items()
                if key in sig.parameters
                and sig.parameters[key].kind
                in {
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.KEYWORD_ONLY,
                }
            }
        )
        return func(**kwargs)
    except Exception as exc:
        function_name = getattr(func, "__name__", type(func).__name__)
        logger.error(
            "Renderer %s failed (%s)",
            function_name,
            type(exc).__name__,
        )
        st.error(
            f"Modul {function_name} tidak dapat dipaparkan "
            f"({type(exc).__name__}). Semak log aplikasi."
        )
        return None


# ======================================================================================
# 4. ENJIN PENYEGERAKAN LANGSUNG 2-HALA: HADDY PRO GOOGLE SHEETS ⟷ STREAMLIT
# ======================================================================================
if "custom_fx_rate" not in st.session_state:
    st.session_state["custom_fx_rate"] = 4.0773
if "risk_drawdown_threshold_pct" not in st.session_state:
    st.session_state["risk_drawdown_threshold_pct"] = 10.0
if "risk_concentration_threshold_pct" not in st.session_state:
    st.session_state["risk_concentration_threshold_pct"] = 30.0
if "holdings_stale_after_minutes" not in st.session_state:
    st.session_state["holdings_stale_after_minutes"] = 15
if "auto_sync_enabled" not in st.session_state:
    st.session_state["auto_sync_enabled"] = True
if "auto_sync_interval" not in st.session_state:
    st.session_state["auto_sync_interval"] = 60
if "sync_cycle_counter" not in st.session_state:
    st.session_state["sync_cycle_counter"] = 0
if "last_sync_epoch" not in st.session_state:
    st.session_state["last_sync_epoch"] = 0.0
if "last_refresh_attempt_epoch" not in st.session_state:
    st.session_state["last_refresh_attempt_epoch"] = 0.0
if "vault_snapshot" not in st.session_state:
    st.session_state["vault_snapshot"] = None
if "vault_snapshot_url" not in st.session_state:
    st.session_state["vault_snapshot_url"] = ""
if "last_sync_time_str" not in st.session_state:
    st.session_state["last_sync_time_str"] = "Belum disegerakkan"
if "gsheets_live_url" not in st.session_state:
    st.session_state["gsheets_live_url"] = get_configured_sheet_url()


def resolve_gsheets_webhook() -> str:
    """Gunakan satu resolver webhook untuk tarikan dan penghantaran barisan."""
    return get_configured_webhook_url()


def parse_gsheets_url(url_str: str):
    """Mengekstrak kunci dokumen dan GID secara dinamik daripada URL Google Sheets."""
    if not url_str:
        return None, None
    doc_match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", str(url_str))
    gid_match = re.search(r"[#&?]gid=([0-9]+)", str(url_str))
    doc_key = doc_match.group(1) if doc_match else None
    gid_val = gid_match.group(1) if gid_match else None
    return doc_key, gid_val


def heal_spreadsheet_formula_errors(df: pd.DataFrame) -> pd.DataFrame:
    """Preserve formula errors for diagnosis; never replace financial values with estimates."""
    if not isinstance(df, pd.DataFrame) or df.empty:
        return df
    return df.copy()


def fetch_direct_sheet_tab(sheet_url: str, tab_name: str = None, gid: str = None) -> pd.DataFrame:
    """Menarik lembaran secara terus daripada URL Google Sheets jika disambungkan."""
    if not is_public_csv_fallback_enabled():
        return pd.DataFrame()
    doc_key, url_gid = parse_gsheets_url(sheet_url)
    if not doc_key:
        return pd.DataFrame()
    target_gid = gid or url_gid
    try:
        if tab_name:
            csv_url = f"https://docs.google.com/spreadsheets/d/{doc_key}/gviz/tq?tqx=out:csv&sheet={quote(tab_name)}"
        elif target_gid:
            csv_url = f"https://docs.google.com/spreadsheets/d/{doc_key}/export?format=csv&gid={target_gid}"
        else:
            csv_url = f"https://docs.google.com/spreadsheets/d/{doc_key}/export?format=csv"
        df_remote = pd.read_csv(csv_url)
        return heal_spreadsheet_formula_errors(df_remote)
    except Exception:
        return pd.DataFrame()


def trigger_auto_refresh_heartbeat(interval_sec: int, enabled: bool) -> int:
    """Memastikan Streamlit melakukan auto-refresh berkala untuk menyegerakkan Google Sheets."""
    if not enabled:
        return st.session_state["sync_cycle_counter"]

    try:
        from streamlit_autorefresh import st_autorefresh
    except ImportError:
        st.warning(
            "Auto-refresh tidak tersedia kerana `streamlit-autorefresh` belum dipasang. "
            "Gunakan butang Segerak sekarang atau pasang kebergantungan projek."
        )
        return st.session_state["sync_cycle_counter"]

    count = st_autorefresh(
        interval=int(interval_sec * 1000),
        limit=None,
        key="haddy_gsheets_autorefresh_engine",
    )
    return int(count or 0)


def fetch_vault_snapshot(live_url: str = ""):
    """
    Pull sekali daripada sumber yang dikonfigurasi. Data snapshot kekal dalam session state
    sehingga sela masa refresh atau permintaan manual berikutnya.
    """
    raw = load_all_terminal_data()
    if not isinstance(raw, dict):
        raw = {"master": raw} if raw is not None else {}

    if live_url:
        _, active_gid = parse_gsheets_url(live_url)
        if active_gid:
            df_gid = fetch_direct_sheet_tab(live_url, gid=active_gid)
            if not df_gid.empty:
                raw[f"gid_{active_gid}"] = df_gid

    for k, val in list(raw.items()):
        if isinstance(val, pd.DataFrame):
            raw[k] = heal_spreadsheet_formula_errors(val)

    cleaned = None
    try:
        sample_df = next(
            (v for v in raw.values() if isinstance(v, pd.DataFrame) and not v.empty),
            None,
        )
        cleaned = smart_invoke(
            process_master_database,
            df=sample_df,
            vault=raw,
            raw_vault=raw,
            data=raw,
        )
    except Exception:
        pass
    return raw, cleaned


def execute_two_way_gsheets_sync(force: bool = False):
    """
    Melaksanakan penyegerakan 2 hala penuh:
    1. PUSH (Streamlit ➔ Google Sheets): Menghantar barisan input luar talian (`sync_queued_inputs`).
    2. PULL (Google Sheets ➔ Streamlit): Menarik data terkini (`load_all_terminal_data` & URL langsung).
    """
    t0 = time.time()
    webhook_url = resolve_gsheets_webhook()
    synced_up_count = 0
    try:
        pending_count = (
            len([f for f in os.listdir(QUEUE_DIR) if f.startswith("pending_")])
            if os.path.exists(QUEUE_DIR)
            else 0
        )
    except Exception:
        pending_count = 0

    interval_sec = max(60, int(st.session_state.get("auto_sync_interval", 60)))
    now_epoch = time.time()
    live_url = st.session_state.get("gsheets_live_url", "")
    previous_snapshot = st.session_state.get("vault_snapshot")
    url_changed = live_url != st.session_state.get("vault_snapshot_url", "")
    refresh_due = should_refresh_snapshot(
        force=force,
        snapshot_exists=isinstance(previous_snapshot, dict),
        url_changed=url_changed,
        auto_sync_enabled=bool(st.session_state.get("auto_sync_enabled", True)),
        now_epoch=now_epoch,
        last_attempt_epoch=st.session_state["last_refresh_attempt_epoch"],
        interval_sec=interval_sec,
    )
    cleaned_df = st.session_state.get("cleaned_master_snapshot")
    if refresh_due:
        st.session_state["last_refresh_attempt_epoch"] = now_epoch
        st.session_state["sync_cycle_counter"] += 1
        try:
            synced_up_count = int(
                sync_queued_inputs(webhook_url, token=get_configured_webhook_token()) or 0
            )
        except Exception:
            synced_up_count = 0

        try:
            pulled_vault, pulled_cleaned_df = fetch_vault_snapshot(live_url)
        except Exception as exc:
            pulled_vault = {"_sync_metadata": {
                "remote_verified": False,
                "source_tier": "No data source available",
                "remote_error": type(exc).__name__,
            }}
            pulled_cleaned_df = None

        sync_metadata = pulled_vault.get("_sync_metadata", {})
        remote_data_confirmed = bool(sync_metadata.get("remote_data_confirmed"))
        if remote_data_confirmed:
            retrieved_at = sync_metadata.get("timestamp") or datetime.now().astimezone().isoformat(
                timespec="seconds"
            )
            sync_metadata["last_successful_sync_at"] = retrieved_at
            st.session_state["last_sync_epoch"] = time.time()
            st.session_state["last_sync_time_str"] = datetime.now().strftime("%H:%M:%S")
            vault_data = pulled_vault
            cleaned_df = pulled_cleaned_df
        elif isinstance(previous_snapshot, dict) and not url_changed:
            vault_data = previous_snapshot.copy()
            previous_metadata = vault_data.get("_sync_metadata", {})
            previous_source_tier = str(
                previous_metadata.get("source_tier", "Sumber tidak diketahui")
            )
            stale_prefix = "Snapshot sesi lama · "
            while previous_source_tier.startswith(stale_prefix):
                previous_source_tier = previous_source_tier[len(stale_prefix):]
            sync_metadata = {
                **previous_metadata,
                "remote_verified": False,
                "remote_data_confirmed": False,
                "data_freshness": "stale_session_snapshot",
                "source_tier": f"{stale_prefix}{previous_source_tier}",
                "remote_error": sync_metadata.get("remote_error") or "remote_pull_not_verified",
                "last_attempt_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            }
            vault_data["_sync_metadata"] = sync_metadata
        else:
            vault_data = pulled_vault
            cleaned_df = pulled_cleaned_df

        vault_data["_sync_metadata"] = sync_metadata
        st.session_state["vault_snapshot"] = vault_data
        st.session_state["cleaned_master_snapshot"] = cleaned_df
        st.session_state["vault_snapshot_url"] = live_url
    else:
        vault_data = previous_snapshot
        sync_metadata = vault_data.get("_sync_metadata", {})

    latency_ms = max(10, int((time.time() - t0) * 1000))
    return vault_data, cleaned_df, synced_up_count, pending_count, latency_ms


# Aktifkan denyutan Auto-Refresh sebelum memuatkan data
current_heartbeat = trigger_auto_refresh_heartbeat(
    interval_sec=int(st.session_state["auto_sync_interval"]),
    enabled=bool(st.session_state["auto_sync_enabled"]),
)

with st.spinner("Memuatkan snapshot terminal..."):
    vault, cleaned_master_df, synced_now, pending_q, sync_latency_ms = execute_two_way_gsheets_sync(force=False)
    fx_rate = float(st.session_state["custom_fx_rate"])
    kpis = extract_portfolio_kpis(vault, fx_rate=fx_rate)

    df_holdings = heal_spreadsheet_formula_errors(get_active_holdings(vault, fx_rate=fx_rate))
    df_cf = heal_spreadsheet_formula_errors(get_cashflow_dataframe(vault))
    df_bursa = heal_spreadsheet_formula_errors(get_top10_bursa(vault))
    df_us = heal_spreadsheet_formula_errors(get_top10_us(vault))
    df_1000 = heal_spreadsheet_formula_errors(build_institutional_screener_data(vault))


def has_source_metric(metric_name: str, label: str) -> bool:
    if kpis.get(metric_name) is None:
        st.info(f"{label} tidak tersedia dalam snapshot sumber; modul ini tidak akan menganggap nilai sebagai sifar.")
        return False
    return True


# ======================================================================================
# 5. BAR SISI (SIDEBAR) — PUSAT KAWALAN AUTO-SYNC GOOGLE SHEETS & NAVIGASI
# ======================================================================================
mode_options = {
    "Overview": "🌐 Paparan Penuh (Semua Kluster)",
    "Portfolio": "📁 Portfolio & Risiko",
    "Pasaran": "📈 Pasaran Saham (Bursa & US)",
    "Kewangan": "🏛️ Bukan Saham (Liabiliti & Bank)",
    "Sistem": "🛠️ Direktori Roh AI & Audit Sync",
}

with st.sidebar:
    if os.path.exists("haddy_logo.png"):
        st.image("haddy_logo.png", width=64, alt="Logo Haddy Pro")
    st.title("Haddy Pro")
    st.caption("Terminal Millx")

    sync_metadata = vault.get("_sync_metadata", {})
    source_tier = str(sync_metadata.get("source_tier", "Sumber tidak diketahui"))
    tabs_loaded = int(sync_metadata.get("tabs_loaded", 0) or 0)
    if sync_metadata.get("remote_data_confirmed") and not sync_metadata.get("cached_tabs"):
        st.success(f"Tarikan Google Sheets disahkan · {tabs_loaded} tab berisi data")
    elif sync_metadata.get("remote_data_confirmed"):
        st.warning(
            f"Sambungan awan disahkan, tetapi {sync_metadata.get('cached_tabs')} tab "
            "menggunakan cache setempat."
        )
    elif sync_metadata.get("remote_verified"):
        st.warning("Webhook menjawab tetapi tiada tab Google Sheets dikenali dipulangkan.")
    elif str(sync_metadata.get("data_freshness", "")).startswith("stale_session"):
        st.warning("Snapshot sesi lama digunakan; tarikan Google Sheets terkini tidak disahkan")
    elif source_tier.startswith("Tier-3"):
        st.warning("Menggunakan cache setempat")
    else:
        st.info("Sumber langsung belum disahkan")
    st.caption(f"Sumber: {source_tier}")
    st.caption(
        f"Tarikan awan terakhir berjaya: {st.session_state['last_sync_time_str']} · "
        f"Barisan luar talian: {pending_q} · Sela: {max(60, int(st.session_state['auto_sync_interval']))}s"
    )
    last_sync_epoch = float(st.session_state.get("last_sync_epoch", 0.0) or 0.0)
    if last_sync_epoch > 0:
        age_seconds = max(0, int(time.time() - last_sync_epoch))
        age_label = (
            f"{age_seconds // 60} min {age_seconds % 60} saat"
            if age_seconds >= 60
            else f"{age_seconds} saat"
        )
        stale_limit_seconds = int(st.session_state["holdings_stale_after_minutes"]) * 60
        if age_seconds > stale_limit_seconds:
            st.warning(
                f"Tarikan terakhir disahkan {age_label} lalu; melebihi ambang "
                f"{st.session_state['holdings_stale_after_minutes']} minit."
            )
        elif not sync_metadata.get("remote_data_confirmed"):
            st.warning(
                f"Tarikan terkini belum disahkan; snapshot terakhir disahkan {age_label} lalu."
            )
        else:
            st.caption(f"Umur tarikan data disahkan: {age_label}.")
    else:
        st.caption("Umur tarikan data disahkan: belum ada dalam sesi ini.")
    if sync_metadata.get("remote_error") and not sync_metadata.get("remote_data_confirmed"):
        st.caption(f"Status tarikan: {sync_metadata['remote_error']}")
    failed_remote_tabs = sync_metadata.get("remote_failed_tabs", [])
    if failed_remote_tabs:
        st.warning(
            "Tab Google Sheets gagal dibaca: "
            + ", ".join(str(tab) for tab in failed_remote_tabs)
        )
    missing_remote_tabs = sync_metadata.get("remote_missing_tabs", [])
    if missing_remote_tabs:
        st.info(
            "Tab pilihan yang tiada dalam spreadsheet: "
            + ", ".join(str(tab) for tab in missing_remote_tabs)
        )

    if synced_now > 0:
        st.toast(f"✅ Auto-Sync: {synced_now} rekod berjaya dihantar ke Google Sheets!", icon="🔄")

    with st.expander("Tetapan penyegerakan", expanded=False):
        url_input = st.text_input(
            "Pautan Google Sheets (pilihan)",
            value=st.session_state["gsheets_live_url"],
            placeholder="Tampal URL Google Sheets...",
            help="Pautan Google Sheets boleh mengandungi #gid=... untuk lembaran tertentu.",
        )
        if url_input.strip() != st.session_state["gsheets_live_url"]:
            st.session_state["gsheets_live_url"] = url_input.strip()
            st.rerun()

        auto_sync_toggle = st.toggle(
            "Auto-sync Google Sheets",
            value=bool(st.session_state["auto_sync_enabled"]),
            help="Semak semula Sheets setiap 60 saat atau lebih ketika aplikasi dibuka; bukan feed harga pasaran.",
        )
        if auto_sync_toggle != st.session_state["auto_sync_enabled"]:
            st.session_state["auto_sync_enabled"] = auto_sync_toggle
            st.rerun()

        interval_choice = st.selectbox(
            "Sela masa auto-sync",
            options=[60, 120, 300],
            index=[60, 120, 300].index(max(60, int(st.session_state["auto_sync_interval"])))
            if max(60, int(st.session_state["auto_sync_interval"])) in [60, 120, 300]
            else 1,
            format_func=lambda x: f"Setiap {x} saat",
        )
        if interval_choice != st.session_state["auto_sync_interval"]:
            st.session_state["auto_sync_interval"] = int(interval_choice)
            st.rerun()

        if st.button("Segerak sekarang", width="stretch", type="primary"):
            synced_vault, _, synced_count, pending_count, _ = execute_two_way_gsheets_sync(force=True)
            sync_metadata = synced_vault.get("_sync_metadata", {})
            source_tier = str(sync_metadata.get("source_tier", "Unknown"))
            tabs_loaded = int(sync_metadata.get("tabs_loaded", 0) or 0)
            if sync_metadata.get("remote_data_confirmed"):
                st.toast(
                    f"Tarikan selesai: {tabs_loaded} tab; {synced_count} rekod luar talian dihantar.",
                    icon="✅",
                )
            else:
                st.toast(
                    "Penyegerakan langsung belum disahkan; aplikasi menggunakan cache setempat.",
                    icon="⚠️",
                )
            if pending_count:
                st.toast(
                    f"{pending_count} transaksi masih menunggu pengesahan Google Sheets.",
                    icon="⚠️",
                )
            st.rerun()

    with st.expander("Tetapan amaran risiko", expanded=False):
        st.number_input(
            "Amaran kerugian berbanding kos (%)",
            min_value=1.0,
            max_value=90.0,
            step=1.0,
            key="risk_drawdown_threshold_pct",
            help="Amaran muncul apabila ROI pegangan sama atau lebih rendah daripada nilai negatif ini.",
        )
        st.number_input(
            "Amaran kepekatan pegangan (%)",
            min_value=1.0,
            max_value=100.0,
            step=1.0,
            key="risk_concentration_threshold_pct",
            help="Bandingkan nilai sesuatu pegangan dengan jumlah nilai pegangan saham.",
        )
        st.number_input(
            "Snapshot dianggap lapuk selepas (minit)",
            min_value=1,
            max_value=1440,
            step=5,
            key="holdings_stale_after_minutes",
            help="Mengukur umur data yang diambil aplikasi, bukan umur sebut harga dalam lembaran.",
        )

    new_fx = st.number_input(
        "Andaian kadar USD/MYR",
        3.0,
        6.0,
        float(fx_rate),
        0.01,
        format="%.4f",
        help="Kadar manual sesi ini; bukan kadar pertukaran langsung.",
    )
    if abs(new_fx - fx_rate) > 1e-5:
        st.session_state["custom_fx_rate"] = new_fx
        st.rerun()

    if st.button("Kunci terminal", width="stretch"):
        st.session_state["vault_authenticated"] = False
        st.rerun()


# ======================================================================================
# 6. PENGEPALA UTAMA, RINGKASAN 00_PUSAT KAWALAN & METRIK BENTO
# ======================================================================================
m_stat = get_dual_market_status()
st.title("Haddy Pro — Terminal Millx")
st.caption("Portfolio, pasaran dan kewangan peribadi")

market_cols = st.columns(2)
for col, label, market in (
    (market_cols[0], "Bursa Malaysia", m_stat["bursa"]),
    (market_cols[1], "Wall Street", m_stat["us"]),
):
    with col:
        with st.container(border=True):
            st.markdown(f"**{label}**")
            st.write(market["status"])
            st.caption(f"{market['time_str']} · anggaran waktu sesi, tidak menyemak cuti bursa")

selected_workspace = st.segmented_control(
    "Ruang kerja",
    options=list(mode_options),
    default="Overview",
    key="dashboard_workspace",
    width="stretch",
)
mode_switch = mode_options.get(selected_workspace, mode_options["Overview"])
render_holding_risk_alerts(
    df_holdings,
    drawdown_threshold_pct=float(st.session_state["risk_drawdown_threshold_pct"]),
    concentration_threshold_pct=float(st.session_state["risk_concentration_threshold_pct"]),
)
st.divider()


# ======================================================================================
# 7. PAPARAN KANDUNGAN MENGIKUT KLUSTER & MOD
# ======================================================================================
if mode_switch == "📁 Portfolio & Risiko":
    st.header("Portfolio & risiko")
    render_portfolio_data_status(
        df_holdings,
        stale_after_minutes=int(st.session_state["holdings_stale_after_minutes"]),
    )
    if not df_holdings.empty:
        total_market_value = float(df_holdings["Nilai_Semasa_MYR"].sum())
        total_unrealized_pnl = float(df_holdings["Untung_Rugi_MYR"].sum())
        summary_cols = st.columns(3)
        summary_cols[0].metric("Pegangan sah", f"{len(df_holdings):,}")
        summary_cols[1].metric("Nilai pegangan saham", f"RM {total_market_value:,.2f}")
        summary_cols[2].metric("Untung/rugi belum realisasi", f"RM {total_unrealized_pnl:,.2f}")
        render_holdings_cards(df_holdings)
        st.plotly_chart(
            render_allocation_donut(df_holdings),
            width="stretch",
            alt="Carta pecahan nilai setiap pegangan saham yang dibaca daripada Google Sheets",
        )
    render_portfolio_manager(df_holdings, fx_rate=fx_rate)
    st.divider()
    render_journal_export(vault)

elif mode_switch == "📈 Pasaran Saham (Bursa & US)":
    t1, t2, t3, t4, t5 = st.tabs(
        [
            "🎯 1. 01_Meja Keputusan",
            "📦 2. 02_Pegangan & 62_Terminal",
            "⚡ 3. Beli, Jual & Moomoo",
            "🗺️ 4. Peta Haba & 1000 Saham",
            "🤖 5. AI, Kuantitatif & 68_Analytics",
        ]
    )
    with t1:
        col_b1, col_b2 = st.columns([7, 3])
        with col_b2:
            if st.button("⚡ TIKET PESANAN PANTAS & KIRA KOS", width="stretch"):
                open_quick_order_modal("", 0.0, fx_rate=fx_rate)
        render_modern_decision_grid(df_bursa, df_us)
        st.plotly_chart(render_rr_comparison_chart(df_bursa, df_us), width="stretch")

    with t2:
        render_holdings_cards(df_holdings)
        st.markdown("---")
        render_trailing_sentinel_ui(vault_data=vault, fx_rate=fx_rate)
        st.markdown("---")
        p1, p2 = st.columns(2)
        with p1:
            st.plotly_chart(render_cumulative_equity_curve(df_cf), width="stretch")
        with p2:
            st.plotly_chart(
                render_allocation_donut(df_holdings),
                width="stretch",
                alt="Carta pecahan nilai setiap pegangan saham",
            )

    with t3:
        sub_td1, sub_td2, sub_td3 = st.tabs(["⚡ Meja Beli & Jual", "🐮 Penjana Moomoo", "🧮 Kalkulator Risiko 3M"])
        with sub_td1:
            render_trade_desk_ui(fx_rate=fx_rate, holdings=df_holdings)
        with sub_td2:
            smart_invoke(render_moomoo_order_generator, fx_rate=fx_rate, vault=vault, kpis=kpis)
        with sub_td3:
            smart_invoke(render_3m_calculator_ui, fx_rate=fx_rate, vault=vault)

    with t4:
        hm1, hm2 = st.tabs(["🗺️ Peta Haba Sektor", "📊 Pengimbas 1,000 Saham Elit"])
        with hm1:
            render_market_heatmap_tab(df_holdings)
        with hm2:
            st.plotly_chart(render_canslim_bubble_matrix(df_1000), width="stretch")
            st.dataframe(df_1000.head(100), width="stretch", hide_index=True)

    with t5:
        qa1, qa2, qa3, qa4 = st.tabs(["💬 Semakan data & DCF", "🎲 Simulasi Kuantitatif", "🎯 Sasaran Sejuta", "📊 Analitik Portfolio"])
        with qa1:
            render_interactive_chat_copilot(fx_rate=fx_rate, vault_data=vault)
            st.markdown("---")
            render_ai_copilot_ui()
        with qa2:
            if has_source_metric("net_invested", "Modal bersih"):
                render_monte_carlo_ui(starting_capital=kpis["net_invested"])
            st.markdown("---")
            render_markowitz_efficient_frontier_ui(vault_data=vault, fx_rate=fx_rate)
            st.markdown("---")
            render_fundamental_health_and_sankey_ui(fx_rate=fx_rate, vault_data=vault)
        with qa3:
            render_milestone_tracker_ui(
                vault,
                current_portfolio_value=kpis.get("active_portfolio_val"),
                fx_rate=fx_rate,
            )
        with qa4:
            render_postmortem_dashboard(fx_rate=fx_rate, vault_data=vault)
            st.markdown("---")
            render_journal_analytics_dashboard(vault_data=vault)

elif mode_switch == "🏛️ Bukan Saham (Liabiliti & Bank)":
    t1, t2, t3, t4 = st.tabs(
        [
            "🏛️ 1. Liabiliti, CCRIS & Strategi Hutang",
            "🏦 2. Simpanan, KWSP & Bank",
            "🌙 3. Zakat & Cukai LHDN",
            "🚨 4. Protokol Krisis & Eksport Laporan",
        ]
    )
    with t1:
        portfolio_value = kpis.get("active_portfolio_val")
        render_debt_management_dashboard(vault, stock_portfolio_val=portfolio_value)
        st.markdown("---")
        smart_invoke(render_debt_payoff_strategies_ui, vault_data=vault)
    with t2:
        render_personal_finance_suite(vault)
    with t3:
        render_zakat_compliance_ui(net_equity=kpis.get("active_portfolio_val"))
        st.markdown("---")
        render_tax_ledger_ui(vault)
    with t4:
        render_report_exporter_ui(vault, kpis, df_bursa, df_us)
        st.markdown("---")
        render_crisis_playbook_ui(net_equity=kpis.get("active_portfolio_val"))

elif mode_switch == "🛠️ Direktori Roh AI & Audit Sync":
    st.subheader("📋 Direktori Navigasi Berpusat Roh AI & Pemetaan 2-Way Google Sheets")
    dir_df = pd.DataFrame(
        [
            {"No.": 1, "Nama Tab Lembaran": "00_Pusat Kawalan", "Kluster": "Induk: Command Center", "Modul Streamlit": "KPI jika tersedia dalam sumber"},
            {"No.": 2, "Nama Tab Lembaran": "62_Terminal Saham", "Kluster": "Kluster 1: Portfolio & Terminal", "Modul Streamlit": "Terminal dan carta"},
            {"No.": 3, "Nama Tab Lembaran": "63_Ringkasan Mudah", "Kluster": "Kluster 1: Portfolio & Terminal", "Modul Streamlit": "Ringkasan portfolio"},
            {"No.": 4, "Nama Tab Lembaran": "02_Pegangan Semasa", "Kluster": "Kluster 1: Portfolio & Terminal", "Modul Streamlit": "Pegangan dan untung/rugi"},
            {"No.": 5, "Nama Tab Lembaran": "66_Aliran Tunai", "Kluster": "Kluster 1: Portfolio & Terminal", "Modul Streamlit": "Deposit dan pengeluaran selesai"},
            {"No.": 6, "Nama Tab Lembaran": "01_Meja Keputusan", "Kluster": "Kluster 2: Strategi & Analisis", "Modul Streamlit": "Keputusan sumber; ralat formula dikekalkan"},
            {"No.": 7, "Nama Tab Lembaran": "Radar_Makro_&_Berita_Live", "Kluster": "Kluster 2: Strategi & Analisis", "Modul Streamlit": "Paparan radar; status sumber di sidebar"},
        ]
    )
    st.dataframe(dir_df, width="stretch", hide_index=True)

    _, current_gid = parse_gsheets_url(st.session_state.get("gsheets_live_url", ""))
    if current_gid and f"gid_{current_gid}" in vault:
        st.markdown("---")
        st.subheader(f"📄 Pratonton Langsung Lembaran Aktif (GID: {current_gid})")
        st.dataframe(vault[f"gid_{current_gid}"], width="stretch", hide_index=True)

    st.markdown("---")
    smart_invoke(render_system_diagnostics, vault=vault, kpis=kpis, fx_rate=fx_rate)
    st.markdown("---")
    render_gold_master_dashboard(kpis, vault, fx_rate=fx_rate)

else:
    # PAPARAN PENUH (6 HAB UTAMA YANG KEMAS & SELARAS DENGAN 3 KLUSTER ROH AI)
    h1, h2, h3, h4, h5, h6 = st.tabs(
        [
            "🎯 1. 01_Meja Keputusan & Trade",
            "📦 2. 02_Pegangan & Aliran Tunai",
            "📡 3. Radar Makro & Peta Haba",
            "🎲 4. Kuantitatif & Risiko",
            "🤖 5. AI Mentor & 68_Analytics",
            "🏛️ 6. Liabiliti, Bank, Zakat & Sistem",
        ]
    )

    with h1:
        col_q1, col_q2 = st.columns([7, 3])
        with col_q2:
            if st.button("⚡ TIKET PESANAN PANTAS & KIRA KOS", width="stretch"):
                open_quick_order_modal("", 0.0, fx_rate=fx_rate)
        render_modern_decision_grid(df_bursa, df_us)
        st.plotly_chart(render_rr_comparison_chart(df_bursa, df_us), width="stretch")
        st.markdown("---")
        tr1, tr2, tr3 = st.tabs(["⚡ Meja Beli & Jual", "🐮 Penjana Pesanan Moomoo", "🧮 Kalkulator Risiko 3M"])
        with tr1:
            render_trade_desk_ui(fx_rate=fx_rate, holdings=df_holdings)
        with tr2:
            smart_invoke(render_moomoo_order_generator, fx_rate=fx_rate, vault=vault, kpis=kpis)
        with tr3:
            smart_invoke(render_3m_calculator_ui, fx_rate=fx_rate, vault=vault)

    with h2:
        render_holdings_cards(df_holdings)
        st.markdown("---")
        render_trailing_sentinel_ui(vault_data=vault, fx_rate=fx_rate)
        st.markdown("---")
        p1, p2 = st.columns(2)
        with p1:
            st.plotly_chart(render_cumulative_equity_curve(df_cf), width="stretch")
        with p2:
            st.plotly_chart(
                render_allocation_donut(df_holdings),
                width="stretch",
                alt="Carta pecahan nilai setiap pegangan saham",
            )
        st.plotly_chart(render_annual_flow_breakdown(df_cf), width="stretch")

    with h3:
        m1, m2, m3 = st.tabs(["📡 Radar_Makro_&_Berita_Live", "🗺️ Peta Haba Sektor", "📊 Pengimbas 1,000 Saham"])
        with m1:
            render_macro_intelligence_dashboard(fx_rate=fx_rate, vault_data=vault)
        with m2:
            render_market_heatmap_tab(df_holdings)
        with m3:
            st.plotly_chart(render_canslim_bubble_matrix(df_1000), width="stretch")
            st.dataframe(df_1000.head(100), width="stretch", hide_index=True)

    with h4:
        q1, q2, q3, q4, q5, q6 = st.tabs(
            [
                "🎲 Monte Carlo & Markowitz",
                "⚡ Matriks Korelasi",
                "🎯 Pengimbas RVOL",
                "📅 Kalendar Earnings",
                "🧪 Backtest Lampau",
                "🏆 Fundamental & aliran tunai",
            ]
        )
        with q1:
            if has_source_metric("net_invested", "Modal bersih"):
                render_monte_carlo_ui(starting_capital=kpis["net_invested"])
            st.markdown("---")
            render_markowitz_efficient_frontier_ui(vault_data=vault, fx_rate=fx_rate)
        with q2:
            render_correlation_matrix_ui(vault_data=vault)
        with q3:
            render_unusual_volume_scanner_ui(vault_data=vault)
        with q4:
            render_earnings_dividend_hub(fx_rate=fx_rate, vault_data=vault)
        with q5:
            render_backtest_ui(vault_data=vault)
        with q6:
            render_fundamental_health_and_sankey_ui(fx_rate=fx_rate, vault_data=vault)

    with h5:
        a1, a2, a3, a4 = st.tabs(
            [
                "💬 Semakan data & DCF",
                "Semakan dagangan & suara",
                "🎯 Sasaran Sejuta",
                "📊 Analitik Portfolio & Audit",
            ]
        )
        with a1:
            render_interactive_chat_copilot(fx_rate=fx_rate, vault_data=vault)
        with a2:
            render_ai_copilot_ui()
            st.markdown("---")
            render_traffic_light_evaluator()
            st.markdown("---")
            render_voice_assistant_ui()
            st.markdown("---")
            render_paper_autopilot_ui()
        with a3:
            render_milestone_tracker_ui(
                vault,
                current_portfolio_value=kpis.get("active_portfolio_val"),
                fx_rate=fx_rate,
            )
        with a4:
            render_postmortem_dashboard(fx_rate=fx_rate, vault_data=vault)
            st.markdown("---")
            render_journal_analytics_dashboard(vault_data=vault)

    with h6:
        f1, f2, f3, f4 = st.tabs(
            [
                "🏛️ Liabiliti, CCRIS & Strategi Hutang",
                "🏦 Simpanan, Bank & KWSP",
                "🌙 Zakat & Cukai LHDN",
                "📑 Laporan Excel, Krisis & Sistem",
            ]
        )
        with f1:
            portfolio_value = kpis.get("active_portfolio_val")
            render_debt_management_dashboard(vault, stock_portfolio_val=portfolio_value)
            st.markdown("---")
            smart_invoke(render_debt_payoff_strategies_ui, vault_data=vault)
        with f2:
            render_personal_finance_suite(vault)
        with f3:
            render_zakat_compliance_ui(net_equity=kpis.get("active_portfolio_val"))
            st.markdown("---")
            render_tax_ledger_ui(vault)
        with f4:
            render_report_exporter_ui(vault, kpis, df_bursa, df_us)
            st.markdown("---")
            render_crisis_playbook_ui(net_equity=kpis.get("active_portfolio_val"))
            st.markdown("---")
            smart_invoke(render_system_diagnostics, vault=vault, kpis=kpis, fx_rate=fx_rate)

st.markdown("---")
st.markdown(
    f"<center><small>Haddy Pro Terminal v4.3 • Snapshot Google Sheets setiap ≥60s ketika sesi aktif ({st.session_state['last_sync_time_str']}) • Status sumber dipaparkan di sidebar</small></center>",
    unsafe_allow_html=True,
)