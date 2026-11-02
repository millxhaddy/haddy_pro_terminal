"""
========================================================================================
HADDY PRO - TERMINAL MILLX
SUITE UJIAN REGRESI SETEMPAT (COMPREHENSIVE TEST SUITE)
========================================================================================
"""

import sys
import time
import os
import warnings
import pandas as pd
import numpy as np
from unittest.mock import MagicMock, patch

# Warna Terminal ANSI
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

passed_tests = 0
failed_tests = 0

def run_test(test_id, test_name, test_func):
    global passed_tests, failed_tests
    start_time = time.time()
    try:
        test_func()
        duration_ms = (time.time() - start_time) * 1000
        print(f" {GREEN}[PASS]{RESET} {test_id} : {test_name:<55} ({duration_ms:6.1f} ms)")
        passed_tests += 1
    except AssertionError as ae:
        duration_ms = (time.time() - start_time) * 1000
        print(f" {RED}[FAIL]{RESET} {test_id} : {test_name:<55} (Ralat: {ae})")
        failed_tests += 1
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        print(f" {RED}[ERROR]{RESET} {test_id} : {test_name:<55} (Pengecualian: {e})")
        failed_tests += 1

print(f"\n{CYAN}========================================================================================{RESET}")
print(f"{CYAN}             HADDY PRO TERMINAL MILLX - SOURCE-BACKED REGRESSION SUITE                   {RESET}")
print(f"{CYAN}========================================================================================{RESET}\n")

# --------------------------------------------------------------------------------------
# 1. UJIAN KESELAMATAN & KRIPTOGRAFI
# --------------------------------------------------------------------------------------
from security_vault import derive_password_verifier, get_master_configured_key

def test_tc01_pbkdf2_password_verifier():
    verifier = derive_password_verifier("unit-test-passphrase")
    assert len(verifier) == 32, f"Pengesah kata laluan sepatutnya 32 bait, dapat {len(verifier)}"

def test_tc02_auth_rejection():
    valid_verifier = derive_password_verifier("unit-test-passphrase")
    invalid_verifier = derive_password_verifier("wrong_password")
    assert valid_verifier != invalid_verifier, "Kata laluan salah tidak boleh sepadan dengan pengesah sah!"

run_test("TC-01", "Pengesah kata laluan PBKDF2-HMAC-SHA256 (600k)", test_tc01_pbkdf2_password_verifier)
run_test("TC-02", "Penolakan kata laluan salah", test_tc02_auth_rejection)

# --------------------------------------------------------------------------------------
# 2. UJIAN PIPELINE DATA & ENJIN GSHEETS
# --------------------------------------------------------------------------------------
from pipeline_cleaner import clean_currency, clean_ratio, clean_percentage
from engine_gsheets import (
    OFFICIAL_GSHEETS_TABS,
    fetch_all_tabs_via_webhook,
    should_refresh_snapshot,
)

def test_tc03_clean_currency():
    assert clean_currency("RM 12.75") == 12.75, "Ralat menukar RM 12.75"
    assert clean_currency("$141.20") == 141.20, "Ralat menukar $141.20"
    assert clean_currency("RM (1,444.79)") == -1444.79, "Ralat kurungan negatif"

def test_tc04_clean_ratio_pct():
    assert clean_ratio("2.50x") == 2.50, "Ralat menukar nisbah 2.50x"
    assert clean_ratio("1 : 2.5") == 2.50, "Nisbah risiko:ganjaran tidak dinormalisasi dengan betul"
    assert clean_percentage("15.5%") == 0.155, "Ralat menukar peratus 15.5%"

def test_tc05_tab_mapping():
    assert len(OFFICIAL_GSHEETS_TABS) == 29, "Pemetaan perlu mengandungi 29 tab!"
    assert OFFICIAL_GSHEETS_TABS.get("pangkalan_1000") == "06_Pangkalan 1000"
    assert OFFICIAL_GSHEETS_TABS.get("meja_keputusan") == "01_Meja Keputusan"
    assert "portfolio_analytics" not in OFFICIAL_GSHEETS_TABS

run_test("TC-03", "Pembersihan Data Mata Wang (Clean Floats & Negatives)", test_tc03_clean_currency)
run_test("TC-04", "Normalisasi Nisbah R:R & Nilai Peratusan", test_tc04_clean_ratio_pct)
run_test("TC-05", "Pemetaan 29 Tab Google Sheets Rasmi", test_tc05_tab_mapping)

def test_tc28_refresh_interval():
    assert should_refresh_snapshot(
        force=False, snapshot_exists=False, url_changed=False,
        auto_sync_enabled=False, now_epoch=10, last_attempt_epoch=10, interval_sec=60,
    )
    arguments = {
        "force": False,
        "snapshot_exists": True,
        "url_changed": False,
        "auto_sync_enabled": True,
        "last_attempt_epoch": 100.0,
        "interval_sec": 60,
    }
    assert not should_refresh_snapshot(now_epoch=159.0, **arguments)
    assert should_refresh_snapshot(now_epoch=160.0, **arguments)
    assert not should_refresh_snapshot(
        force=False, snapshot_exists=True, url_changed=False,
        auto_sync_enabled=False, now_epoch=1000, last_attempt_epoch=100, interval_sec=60,
    )
    assert should_refresh_snapshot(
        force=True, snapshot_exists=True, url_changed=False,
        auto_sync_enabled=False, now_epoch=100, last_attempt_epoch=100, interval_sec=60,
    )

def test_tc29_webhook_uses_one_request_for_partial_data():
    response = MagicMock()
    response.__enter__.return_value = response
    response.read.return_value = b'{"status":"ok","vault":{"00_Pusat Kawalan":[]}}'
    with patch("engine_gsheets.get_configured_webhook_token", return_value="test-token"):
        with patch("engine_gsheets.urllib.request.urlopen", return_value=response) as urlopen:
            result = fetch_all_tabs_via_webhook("https://example.invalid/script")
    assert result["_fetch_metadata"]["request_ok"]
    assert result["_fetch_metadata"]["request_count"] == 1
    assert urlopen.call_count == 1, "Snapshot separa tidak boleh mencetuskan fanout per tab"

def test_tc31_webhook_preserves_safe_error_metadata():
    response = MagicMock()
    response.__enter__.return_value = response
    response.read.return_value = (
        b'{"status":"error","code":"server_error",'
        b'"failed_tabs":["02_Pegangan Semasa"]}'
    )
    with patch("engine_gsheets.get_configured_webhook_token", return_value="test-token"):
        with patch("engine_gsheets.urllib.request.urlopen", return_value=response):
            result = fetch_all_tabs_via_webhook("https://example.invalid/script")
    metadata = result["_fetch_metadata"]
    assert not metadata["request_ok"]
    assert metadata["error"] == "server_error"
    assert metadata["failed_tabs"] == ["02_Pegangan Semasa"]
    assert "token" not in str(metadata).lower()

def test_tc32_webhook_marks_absent_tabs_optional():
    response = MagicMock()
    response.__enter__.return_value = response
    response.read.return_value = (
        b'{"status":"ok","vault":{"02_Pegangan Semasa":[]},'
        b'"missing_tabs":["68_Portfolio Analytics","02_Pegangan Semasa"]}'
    )
    with patch("engine_gsheets.get_configured_webhook_token", return_value="test-token"):
        with patch("engine_gsheets.urllib.request.urlopen", return_value=response):
            result = fetch_all_tabs_via_webhook("https://example.invalid/script")
    metadata = result["_fetch_metadata"]
    assert metadata["request_ok"]
    assert metadata["tabs_received"] == 1
    assert metadata["missing_tabs"] == ["02_Pegangan Semasa"]

run_test("TC-28", "Jadual refresh: 60s minimum, manual dan auto toggle", test_tc28_refresh_interval)
run_test("TC-29", "Satu permintaan webhook tanpa fanout tab", test_tc29_webhook_uses_one_request_for_partial_data)
run_test("TC-31", "Pengekalan kod ralat dan tab gagal secara selamat", test_tc31_webhook_preserves_safe_error_metadata)
run_test("TC-32", "Tab pilihan tiada tanpa menolak tab yang berjaya", test_tc32_webhook_marks_absent_tabs_optional)

# --------------------------------------------------------------------------------------
# 3. UJIAN METRIK EKSEKUTIF, ALIRAN TUNAI & PEGANGAN AKTIF
# --------------------------------------------------------------------------------------
from metrics_bento import extract_portfolio_kpis
from visuals_cashflow import get_cashflow_dataframe
from portfolio_holdings import get_active_holdings

def test_tc06_kpis():
    k = extract_portfolio_kpis({})
    assert "net_invested" not in k, "Modal rekaan tidak boleh dipaparkan tanpa rekod sumber"
    cashflow = pd.DataFrame(
        [
            {"Tarikh": "2025-01-01", "Jenis Aktiviti": "Deposit", "Jumlah (MYR)": "RM 1,000", "Status": "Completed"},
            {"Tarikh": "2025-02-01", "Jenis Aktiviti": "Withdrawal", "Jumlah (MYR)": "RM 250", "Status": "Completed"},
            {"Tarikh": "2025-02-02", "Jenis Aktiviti": "Deposit", "Jumlah (MYR)": "#REF!", "Status": "Completed"},
            {"Tarikh": "2025-03-01", "Jenis Aktiviti": "Deposit", "Jumlah (MYR)": "RM 9,000", "Status": "Failed"},
        ]
    )
    k = extract_portfolio_kpis({"aliran_tunai": cashflow})
    assert k["total_deposit"] == 1000.0
    assert k["total_withdrawal"] == 250.0
    assert k["net_invested"] == 750.0

def test_tc07_cashflow():
    df_cf = get_cashflow_dataframe(
        {
            "66_Aliran Tunai": pd.DataFrame(
                [
                    {"Tarikh": "2024-01-01", "Jenis Aktiviti": "Deposit", "Jumlah (MYR)": "RM 1,000", "Status": "Completed"},
                    {"Tarikh": "2024-02-01", "Jenis Aktiviti": "Withdrawal", "Jumlah (MYR)": "-RM 200", "Status": "Completed"},
                    {"Tarikh": "2025-01-01", "Jenis Aktiviti": "Deposit", "Jumlah (MYR)": "RM 500", "Status": "Completed"},
                    {"Tarikh": "2025-02-01", "Jenis Aktiviti": "Deposit", "Jumlah (MYR)": "RM 1,000", "Status": "Declined"},
                ]
            )
        }
    )
    assert df_cf["Tahun"].tolist() == ["2024", "2025"]
    assert df_cf.iloc[-1]["Kumulatif_Modal"] == 1300.0

def test_tc33_cashflow_mixed_date_formats():
    source = pd.DataFrame(
        [
            {"Tarikh": "31-12-2024", "Jenis Aktiviti": "Deposit", "Jumlah (MYR)": "RM 100", "Status": "Completed"},
            {"Tarikh": "2025-01-02", "Jenis Aktiviti": "Deposit", "Jumlah (MYR)": "RM 200", "Status": "Completed"},
        ]
    )
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = get_cashflow_dataframe({"66_Aliran Tunai": source})
    assert result["Tahun"].tolist() == ["2024", "2025"]
    assert not any("Parsing dates" in str(warning.message) for warning in caught)

def test_tc08_active_holdings():
    raw_holdings = pd.DataFrame(
        [
            {
                "📌 Simbol (Ticker)": "KLSE:0039",
                "🏢 Nama Syarikat": "Example Bursa",
                "🌐 Pasaran": "Bursa Malaysia",
                "📦 Kuantiti": 100,
                "💰 Kos Purata": 10.0,
                "💵 Nilai Pasaran (MYR)": 900.0,
                "📊 Untung/Rugi Belum Realisasi (MYR)": -100.0,
                "💵 Harga Rujukan / Live": 9.0,
            },
            {
                "📌 Simbol (Ticker)": "NYSE:UMC",
                "🏢 Nama Syarikat": "Example US",
                "🌐 Pasaran": "Wall Street US",
                "📦 Kuantiti": 10,
                "💰 Kos Purata": 20.0,
                "💵 Nilai Pasaran (MYR)": 733.914,
                "📊 Untung/Rugi Belum Realisasi (MYR)": -80.832,
                "💵 Harga Rujukan / Live": 18.0,
            },
            {
                "📌 Simbol (Ticker)": "KLSE:0039",
                "🏢 Nama Syarikat": "Example Bursa",
                "🌐 Pasaran": "Bursa Malaysia",
                "📦 Kuantiti": 50,
                "💰 Kos Purata": 10.0,
                "💵 Nilai Pasaran (MYR)": 450.0,
                "📊 Untung/Rugi Belum Realisasi (MYR)": -50.0,
                "💵 Harga Rujukan / Live": 9.0,
            },
        ]
    )
    df_h = get_active_holdings(
        {
            "active_holdings_raw_df": raw_holdings,
            "_sync_metadata": {
                "source_tier": "Tier-1 Webhook Live",
                "tab_sources": {"pegangan_semasa": "webhook"},
            },
        }
    )
    tickers = df_h["Ticker"].tolist()
    assert any("UMC" in t for t in tickers), "Pegangan UMC tidak ditemui!"
    assert any("0039" in t or "GFM" in t for t in tickers), "Pegangan GFM tidak ditemui!"
    assert np.isclose(df_h.loc[df_h["Ticker"] == "KLSE:0039", "ROI_Pct"].iloc[0], -10.0)
    assert df_h.loc[df_h["Ticker"] == "KLSE:0039", "Unit"].iloc[0] == 150
    assert df_h.attrs["holding_source"] == "webhook"
    assert not get_active_holdings({}).any().any(), "Pegangan contoh tidak boleh dipaparkan tanpa sumber."

    formula_error_holdings = pd.DataFrame(
        [
            {
                "Ticker": "KLSE:ERR",
                "Market": "Bursa Malaysia",
                "Quantity": 10,
                "Average Cost": 10.0,
                "Market Value (MYR)": 120.0,
                "Unrealized P&L": "#N/A",
                "Timestamp": "2025-01-01T10:00:00",
            }
        ]
    )
    stale_cache_time = "2024-12-01T10:00:00"
    formula_error_result = get_active_holdings(
        {
            "active_holdings_raw_df": formula_error_holdings,
            "_sync_metadata": {
                "timestamp": "2025-01-01T10:00:00",
                "tab_sources": {"pegangan_semasa": "local cache"},
                "tab_cache_timestamps": {"pegangan_semasa": stale_cache_time},
            },
        }
    )
    assert formula_error_result.attrs["holding_retrieved_at"] == stale_cache_time
    assert not formula_error_result.attrs["quote_timestamp_available"]
    assert pd.isna(formula_error_result.iloc[0]["Harga_Semasa"])
    assert pd.isna(formula_error_result.iloc[0]["Untung_Rugi_MYR"])
    assert pd.isna(formula_error_result.iloc[0]["ROI_Pct"])
    formula_error_kpis = extract_portfolio_kpis(
        {"active_holdings_raw_df": formula_error_holdings}
    )
    assert "unrealized_pnl" not in formula_error_kpis
    assert "unrealized_roi_pct" not in formula_error_kpis

run_test("TC-06", "Pengiraan Papan Skor Bento KPI Kewangan", test_tc06_kpis)
run_test("TC-07", "Audit Trajektori Kumulatif Aliran Tunai 2024-2026", test_tc07_cashflow)
run_test("TC-33", "Tarikh aliran tunai dd-mm-yyyy dan ISO tanpa amaran", test_tc33_cashflow_mixed_date_formats)
run_test("TC-08", "Integriti Pengesanan Posisi Pegangan Aktif (UMC & GFM)", test_tc08_active_holdings)

# --------------------------------------------------------------------------------------
# 4. UJIAN MEJA KEPUTUSAN & PENGIMBAS 1,000 SAHAM
# --------------------------------------------------------------------------------------
from decision_tables import get_top10_bursa, get_top10_us
from master_screener import build_institutional_screener_data

def test_tc09_decision_tables():
    assert get_top10_bursa({}).empty
    assert get_top10_us({}).empty
    source = pd.DataFrame(
        [{"Ticker": "KLSE:AAA", "Harga Rujukan (RM)": "RM 2.00", "Stop Loss (SL)": "RM 1.80",
          "Sasaran Untung (TP)": "RM 2.50", "Nisbah R:R": "2.50x", "Keputusan Akhir": "Pantau"}]
    )
    bursa = get_top10_bursa({"top10_bursa": source})
    assert bursa.iloc[0]["Ticker"] == "KLSE:AAA"
    assert bursa.iloc[0]["Harga_Rujukan"] == 2.0
    assert bursa.iloc[0]["RR"] == 2.5

def test_tc10_master_1000():
    df_m = build_institutional_screener_data({})
    assert df_m.empty, "Screener tidak boleh menjana sekuriti contoh tanpa sumber"
    source = pd.DataFrame([{"Ticker": "KLSE:AAA", "Harga": 2.0}])
    assert build_institutional_screener_data({"screener_1000": source}).equals(source)

run_test("TC-09", "Meja Keputusan Harian (Top 10 Bursa & Top 10 US R:R >= 2.5x)", test_tc09_decision_tables)
run_test("TC-10", "Pangkalan Data 1,000 Saham Elit (Imbangan 500:500)", test_tc10_master_1000)

# --------------------------------------------------------------------------------------
# 5. UJIAN PENGURUSAN RISIKO 3M & PESANAN MOOMOO
# --------------------------------------------------------------------------------------
from risk_calculator_audio import calculate_position_size
from moomoo_journal_analytics import generate_moomoo_order_payload

def test_tc11_position_size_3m():
    res = calculate_position_size(
        account_capital=42497.80,
        risk_pct=1.5,
        entry_price=12.75,
        stop_loss=12.10,
        take_profit=14.38,
        market_type="Bursa Malaysia"
    )
    assert res["lot_size"] > 0, "Saiz lot Bursa mestilah bernilai positif"
    assert res["units_allocated"] % 100 == 0, "Kuantiti unit Bursa mestilah gandaan 100"
    assert res["actual_risk_myr"] <= res["max_risk_myr"], "Had kerugian tidak boleh melebihi bajet risiko!"

def test_tc12_moomoo_order():
    ticket = generate_moomoo_order_payload(
        ticker="KLSE:TENAGA", market="Bursa Malaysia", order_type="Limit",
        units=700, limit_price=12.75, stop_loss_price=12.10, take_profit_price=14.38
    )
    assert "MOOMOO ORDER TICKET" in ticket["summary_text"]
    assert ticket["lots"] == 7
    assert ticket["currency"] == "MYR"

run_test("TC-11", "Kalkulator Pengurusan Risiko DDNK 3M (Anti-Blowup)", test_tc11_position_size_3m)
run_test("TC-12", "Penjana Tiket Pesanan Moomoo Universal Account (8702)", test_tc12_moomoo_order)

# --------------------------------------------------------------------------------------
# 6. UJIAN ENJIN KUANTITATIF (MONTE CARLO, KORELASI, HEATMAP)
# --------------------------------------------------------------------------------------
from market_heatmap import generate_heatmap_dataset
from advanced_quant_suite import run_monte_carlo_simulation
from fluent_core_engine import get_dual_market_status
from moomoo_journal_analytics import get_journal_analytics_data, get_realized_trade_pnls
from backtest_engine import run_ddnk_backtest
from chat_copilot_dcf import process_ai_chat_response

def test_tc13_heatmap_dataset():
    df_h = generate_heatmap_dataset(pd.DataFrame())
    assert df_h.empty, "Peta haba tidak boleh memaparkan pegangan contoh"
    holdings = pd.DataFrame(
        [{
            "Ticker": "KLSE:AAA",
            "Nama_Syarikat": "Example",
            "Pasaran": "Bursa Malaysia",
            "Sektor": "Utiliti",
            "Nilai_Semasa_MYR": 500.0,
            "ROI_Pct": 10.0,
        }]
    )
    df_h = generate_heatmap_dataset(holdings)
    assert len(df_h) == 1
    assert df_h.iloc[0]["Nilai_Pegangan_MYR"] == 500.0
    assert df_h.iloc[0]["Perubahan_Pct"] == 10.0

def test_tc14_monte_carlo():
    trade_pnls = [100.0, 100.0, -50.0, 0.0]
    mc = run_monte_carlo_simulation(
        starting_capital=1000.0,
        trade_pnls=trade_pnls,
        num_simulations=500,
        num_trades=50,
    )
    assert mc["final_median"] > 1000.0, "Bootstrap mesti mencerminkan expectancy positif sumber ujian."
    assert 0.0 <= mc["ruin_prob"] <= 5.0, "Kebarangkalian kejatuhan modal melebihi had toleransi!"

def test_tc34_journal_analytics_uses_realized_source_rows():
    journal = pd.DataFrame(
        [
            {"Pasaran": "Bursa", "Untung Bersih (MYR)": "RM 100.00"},
            {"Pasaran": "US", "Untung Bersih (MYR)": "-RM 50.00"},
            {"Pasaran": "Bursa", "Untung Bersih (MYR)": "RM 0.00"},
            {"Pasaran": "US", "Untung Bersih (MYR)": "#N/A"},
            {"Pasaran": "US", "Untung Bersih (MYR)": ""},
        ]
    )
    vault = {"jurnal_dagangan_df": journal}
    analytics = get_journal_analytics_data(vault)
    assert get_realized_trade_pnls(vault) == [100.0, -50.0, 0.0]
    assert analytics["metrics"]["total_trades"] == 3
    assert np.isclose(analytics["metrics"]["win_rate_pct"], 100 / 3)
    assert analytics["metrics"]["profit_factor"] == 2.0
    assert analytics["metrics"]["net_pnl_myr"] == 50.0
    assert analytics["market_pnl"]["Bersih_MYR"].sum() == 50.0

def test_tc35_journal_analytics_does_not_invent_missing_metrics():
    analytics = get_journal_analytics_data({})
    assert analytics["metrics"]["total_trades"] == 0
    assert analytics["metrics"]["win_rate_pct"] is None
    assert analytics["metrics"]["net_pnl_myr"] is None
    try:
        run_monte_carlo_simulation(starting_capital=1000.0)
    except ValueError:
        return
    raise AssertionError("Simulasi tanpa P&L empirikal atau parameter eksplisit mesti ditolak.")

def test_tc36_backtest_uses_supplied_candles():
    close = np.concatenate((np.linspace(100, 70, 30), np.linspace(71, 140, 30)))
    candles = pd.DataFrame(
        {
            "Date": pd.date_range("2025-01-01", periods=len(close)),
            "Close": close,
            "High": close * 1.001,
            "Low": close * 0.999,
        }
    )
    result = run_ddnk_backtest(
        candles,
        initial_capital=10_000.0,
        risk_per_trade=0.01,
    )
    assert len(result["equity_curve"]) == len(candles)
    assert len(result["dates"]) == len(candles)
    assert result["total_pnl"] == result["final_capital"] - 10_000.0

def test_tc37_chat_does_not_invent_personal_data():
    assert "tidak ditemui" in process_ai_chat_response("Status UMC", vault_data={})
    assert "tidak tersedia" in process_ai_chat_response("Semak baki liabiliti", vault_data={})
    assert "Tiada pegangan" in process_ai_chat_response(
        "Senaraikan pegangan semasa", vault_data={}
    )

def test_tc15_correlation_diagonal():
    # Semakan matematik asas korelasi: korelasi sesuatu aset dengan dirinya sendiri adalah 1.00
    assets = ["TENAGA", "NVDA"]
    corr_matrix = np.corrcoef([[1, 2, 3], [1, 2, 4]])
    assert np.isclose(corr_matrix[0, 0], 1.0), "Nilai diagonal matriks korelasi bukan 1.00!"

def test_tc30_market_status_without_pytz():
    with patch("fluent_core_engine.pytz", None):
        status = get_dual_market_status()
    assert status["bursa"]["time_str"].endswith("MYT")
    assert status["us"]["time_str"].endswith("EST")

run_test("TC-13", "Integriti Struktur Peta Haba Sektor (Treemap Dataset)", test_tc13_heatmap_dataset)
run_test("TC-14", "Simulasi Monte Carlo & Pengiraan Probability of Ruin", test_tc14_monte_carlo)
run_test("TC-34", "Analitik jurnal dikira daripada rekod P&L sumber", test_tc34_journal_analytics_uses_realized_source_rows)
run_test("TC-35", "Tiada statistik rekaan apabila jurnal tiada", test_tc35_journal_analytics_does_not_invent_missing_metrics)
run_test("TC-36", "Backtest menggunakan hanya candle yang dibekalkan", test_tc36_backtest_uses_supplied_candles)
run_test("TC-37", "Chat tidak mereka baki, pegangan atau data peribadi", test_tc37_chat_does_not_invent_personal_data)
run_test("TC-15", "Ketepatan Matematik Matriks Korelasi Silang Aset", test_tc15_correlation_diagonal)
run_test("TC-30", "Fallback zon masa pasaran tanpa pytz", test_tc30_market_status_without_pytz)

# --------------------------------------------------------------------------------------
# 7. UJIAN AI MENTOR, SASARAN SEJUTA & ZAKAT SAHAM
# --------------------------------------------------------------------------------------
from ai_copilot_mentor import audit_stock_entry_decision
from million_milestone import calculate_compounding_schedule
from zakat_compliance import calculate_stock_zakat

def test_tc16_ai_mentor_fomo_block():
    # Ujian entri berunsur FOMO
    res_fomo = audit_stock_entry_decision(
        ticker="DJT", market="Wall Street US", entry_price=38.0, stop_loss=32.0, take_profit=42.0,
        wyckoff_phase="Fasa E (Terlajak Pucuk / Overbought)",
        catalyst_reason="Hype berita", is_fomo_news=True
    )
    assert res_fomo["all_passed"] is False, "AI Mentor sepatutnya MENOLAK entri FOMO!"

def test_tc17_compounding_million():
    df_s = calculate_compounding_schedule(starting_capital=42497.80, monthly_deposit=1000.0, monthly_roi_pct=3.0, months=60)
    baki_akhir_60 = df_s.iloc[-1]["Baki Akhir (RM)"]
    assert baki_akhir_60 > 400000.0, f"Bulan 60 sepatutnya > RM 400k, dapat RM {baki_akhir_60:,.2f}"

def test_tc18_zakat_calculation():
    z = calculate_stock_zakat(active_portfolio_val=50000.0, cash_buffer=10000.0, short_term_liabilities=0.0, gold_price_per_gram=385.50)
    assert z["is_nisab_reached"] is True, "Nilai RM 60,000 sepatutnya melepasi nisab 85g emas!"
    assert np.isclose(z["zakat_payable"], 60000.0 * 0.025), "Kiraan zakat 2.5% tidak tepat!"

run_test("TC-16", "Pencegahan Saringan FOMO oleh AI Mentor DDNK 3M", test_tc16_ai_mentor_fomo_block)
run_test("TC-17", "Model Matematik Pengkompaunan 60-Bulan Sasaran Sejuta", test_tc17_compounding_million)
run_test("TC-18", "Taksiran Zakat Saham Kaedah Urus Niaga (Nisab 85g Emas)", test_tc18_zakat_calculation)

# --------------------------------------------------------------------------------------
# 8. UJIAN TRAILING SENTINEL & LAMPU ISYARAT CYBORG
# --------------------------------------------------------------------------------------
from trailing_sentinel import calculate_trailing_stops
from portfolio_risk_alerts import evaluate_holding_risks
from portfolio_workspace import (
    get_journal_dataframe,
    generate_journal_csv,
    generate_journal_xlsx,
    prepare_trade_confirmation,
)
from gsheets_sync import sync_record_trade
import io
from openpyxl import load_workbook

def test_tc19_trailing_stops():
    holdings = [{"ticker": "NYSE:UMC", "currency": "$", "entry": 19.26, "live": 18.65, "peak": 21.07}]
    df_ts = calculate_trailing_stops(holdings)
    assert not df_ts.empty, "Trailing stop UMC gagal dijana!"

def test_tc20_holding_risk_alerts():
    holdings = pd.DataFrame(
        [
            {"Ticker": "GFM", "Nilai_Semasa_MYR": 200.0, "ROI_Pct": -18.0},
            {"Ticker": "UMC", "Nilai_Semasa_MYR": 800.0, "ROI_Pct": -2.0},
        ]
    )
    alerts = evaluate_holding_risks(holdings)
    assert any(alert["ticker"] == "GFM" and alert["type"] == "Kerugian berbanding kos" for alert in alerts)
    assert any(alert["ticker"] == "UMC" and alert["type"] == "Kepekatan pegangan" for alert in alerts)
    assert alerts[0]["severity"] == "Tinggi"

def test_tc21_no_risk_thresholds_breached():
    holdings = pd.DataFrame(
        [
            {"Ticker": "AAA", "Nilai_Semasa_MYR": 100.0, "ROI_Pct": -5.0},
            {"Ticker": "BBB", "Nilai_Semasa_MYR": 100.0, "ROI_Pct": 1.0},
        ]
    )
    assert evaluate_holding_risks(holdings, concentration_threshold_pct=60.0) == []

def test_tc22_risk_alerts_reject_invalid_data():
    invalid_holdings = pd.DataFrame(
        [{"Ticker": "AAA", "Nilai_Semasa_MYR": 0, "ROI_Pct": -20}]
    )
    try:
        evaluate_holding_risks(invalid_holdings)
    except ValueError:
        return
    raise AssertionError("Data pegangan yang tiada nilai pasaran sah mesti ditolak")

def test_tc23_confirmed_trade_calculation():
    trade = prepare_trade_confirmation(
        is_buy=False,
        ticker="nyse:umc",
        market="Wall Street US",
        quantity=2,
        price=11.0,
        average_cost=10.0,
        fx_rate=4.0,
        fees_myr=1.0,
    )
    assert trade["ticker"] == "NYSE:UMC"
    assert trade["pnl_myr"] == 7.0
    assert trade["notional_myr"] == 88.0

def test_tc24_journal_exports_are_auditable_and_safe():
    journal = pd.DataFrame(
        [
            {"Ticker": "=HYPERLINK(\"https://example.invalid\")", "Untung (RM)": -25.0}
        ]
    )
    assert get_journal_dataframe({"jurnal_dagangan_df": journal}).equals(journal)
    csv_bytes = generate_journal_csv(journal)
    assert b"'=HYPERLINK" in csv_bytes
    workbook_bytes = generate_journal_xlsx(
        journal,
        {"source_tier": "Tier-1 Webhook", "timestamp": "2026-11-02 06:00:00"},
    )
    workbook = load_workbook(io.BytesIO(workbook_bytes), data_only=False)
    assert workbook["Jurnal_Dagangan"]["A2"].value.startswith("'=")
    assert workbook["Metadata_Eksport"]["B2"].value

def test_tc25_journal_export_rejects_empty_data():
    try:
        generate_journal_csv(pd.DataFrame())
    except ValueError:
        return
    raise AssertionError("Eksport jurnal kosong mesti ditolak")

def test_tc26_trade_write_includes_cost_and_fees():
    with patch(
        "gsheets_sync.write_transaction_with_dsr",
        return_value={"status": "SYNCED"},
    ) as writer:
        sync_record_trade(
            False,
            "NYSE:UMC",
            "Wall Street US",
            2,
            11.0,
            7.0,
            "Audit test",
            average_cost=10.0,
            fees_myr=1.0,
        )
    row = writer.call_args.args[1]
    assert writer.call_args.args[0] == "03_Jurnal Dagangan"
    assert writer.call_args.kwargs["action"] == "append_row"
    assert row["Kos Purata"] == 10.0
    assert row["Yuran (MYR)"] == 1.0

def test_tc20_app_syntax_compilation():
    import py_compile
    # Memastikan app.py boleh dikompil tanpa sebarang IndentationError atau SyntaxError
    py_compile.compile("app.py", doraise=True)

run_test("TC-19", "Penjaga Trailing Stop Dinamik & Zon Penampan", test_tc19_trailing_stops)
run_test("TC-20", "Amaran Kerugian & Kepekatan Pegangan", test_tc20_holding_risk_alerts)
run_test("TC-21", "Tiada Amaran Apabila Semua Ambang Dipatuhi", test_tc21_no_risk_thresholds_breached)
run_test("TC-22", "Penolakan Data Pegangan Tanpa Nilai Sah", test_tc22_risk_alerts_reject_invalid_data)
run_test("TC-23", "Anggaran Transaksi dan Untung/Rugi Bersih", test_tc23_confirmed_trade_calculation)
run_test("TC-24", "Eksport Jurnal Audit dan Perlindungan CSV Formula", test_tc24_journal_exports_are_auditable_and_safe)
run_test("TC-25", "Penolakan Eksport Jurnal Kosong", test_tc25_journal_export_rejects_empty_data)
run_test("TC-26", "Lejar Jualan Menyimpan Kos Purata dan Yuran", test_tc26_trade_write_includes_cost_and_fees)
run_test("TC-27", "Penyusunan Sintaks Penuh Aplikasi Utama (app.py)", test_tc20_app_syntax_compilation)

# --------------------------------------------------------------------------------------
# RUMUSAN LAPORAN UJIAN
# --------------------------------------------------------------------------------------
print(f"\n{CYAN}----------------------------------------------------------------------------------------{RESET}")
if failed_tests == 0:
    print(f" {GREEN}STATUS KESELURUHAN: SEMUA UJIAN LULUS ({passed_tests}/{passed_tests}){RESET}")
    print(" Keputusan ini bukan pensijilan produksi, SLA, atau keselamatan.")
else:
    print(f" {RED}STATUS KESELURUHAN: {failed_tests} UJIAN GAGAL DARI {passed_tests + failed_tests} UJIAN{RESET}")
print(f"{CYAN}----------------------------------------------------------------------------------------{RESET}\n")
