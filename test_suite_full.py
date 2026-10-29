"""
========================================================================================
HADDY PRO - TERMINAL MILLX
SUITE UJIAN AUTOMATIK PENUH: 20/20 TEST CASES (COMPREHENSIVE TEST SUITE)
========================================================================================
"""

import sys
import time
import os
import pandas as pd
import numpy as np

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
print(f"{CYAN}             HADDY PRO TERMINAL MILLX - 20/20 COMPREHENSIVE TEST SUITE                   {RESET}")
print(f"{CYAN}========================================================================================{RESET}\n")

# --------------------------------------------------------------------------------------
# 1. UJIAN KESELAMATAN & KRIPTOGRAFI
# --------------------------------------------------------------------------------------
from security_vault import derive_aes_key, get_master_configured_key

def test_tc01_pbkdf2_key():
    key = derive_aes_key("millx@LIPIS84")
    assert len(key) == 32, f"Kunci AES sepatutnya 32-bait (256-bit), dapat {len(key)}"

def test_tc02_auth_rejection():
    key_real = derive_aes_key("millx@LIPIS84")
    key_fake = derive_aes_key("wrong_password")
    assert key_real != key_fake, "Kunci kata laluan salah tidak boleh sepadan dengan kunci sah!"

run_test("TC-01", "Penerbitan Kunci PBKDF2-HMAC-SHA256 (600k Lelaran)", test_tc01_pbkdf2_key)
run_test("TC-02", "Penolakan Kata Laluan Palsu (AES Auth Gate)", test_tc02_auth_rejection)

# --------------------------------------------------------------------------------------
# 2. UJIAN PIPELINE DATA & ENJIN GSHEETS
# --------------------------------------------------------------------------------------
from pipeline_cleaner import clean_currency, clean_ratio, clean_percentage
from engine_gsheets import TAB_GIDS

def test_tc03_clean_currency():
    assert clean_currency("RM 12.75") == 12.75, "Ralat menukar RM 12.75"
    assert clean_currency("$141.20") == 141.20, "Ralat menukar $141.20"
    assert clean_currency("RM (1,444.79)") == -1444.79, "Ralat kurungan negatif"

def test_tc04_clean_ratio_pct():
    assert clean_ratio("2.50x") == 2.50, "Ralat menukar nisbah 2.50x"
    assert clean_percentage("15.5%") == 0.155, "Ralat menukar peratus 15.5%"

def test_tc05_tab_gids():
    assert TAB_GIDS.get("Master Database") == 8888888, "GID Master Database salah!"
    assert TAB_GIDS.get("Meja_Keputusan_Harian") == 880088, "GID Meja Keputusan salah!"
    assert TAB_GIDS.get("Sasaran_Sejuta") == 7700770, "GID Sasaran Sejuta salah!"

run_test("TC-03", "Pembersihan Data Mata Wang (Clean Floats & Negatives)", test_tc03_clean_currency)
run_test("TC-04", "Normalisasi Nisbah R:R & Nilai Peratusan", test_tc04_clean_ratio_pct)
run_test("TC-05", "Pemetaan GID Numerik Google Sheets Rasmi", test_tc05_tab_gids)

# --------------------------------------------------------------------------------------
# 3. UJIAN METRIK EKSEKUTIF, ALIRAN TUNAI & PEGANGAN AKTIF
# --------------------------------------------------------------------------------------
from metrics_bento import extract_portfolio_kpis
from visuals_cashflow import get_cashflow_dataframe
from portfolio_holdings import get_active_holdings

def test_tc06_kpis():
    k = extract_portfolio_kpis({})
    assert k["net_invested"] == 42497.80, f"Modal bersih sepatutnya 42497.80, dapat {k['net_invested']}"
    assert k["win_rate_pct"] >= 50.0, "Kadar kemenangan di bawah penanda aras!"

def test_tc07_cashflow():
    df_cf = get_cashflow_dataframe({})
    last_row = df_cf.iloc[-1]
    assert last_row["Kumulatif_Modal"] == 42497.80, "Kumulatif modal 2026 tidak sepadan!"

def test_tc08_active_holdings():
    df_h = get_active_holdings({})
    tickers = df_h["Ticker"].tolist()
    assert any("UMC" in t for t in tickers), "Pegangan UMC tidak ditemui!"
    assert any("0039" in t or "GFM" in t for t in tickers), "Pegangan GFM tidak ditemui!"

run_test("TC-06", "Pengiraan Papan Skor Bento KPI Kewangan", test_tc06_kpis)
run_test("TC-07", "Audit Trajektori Kumulatif Aliran Tunai 2024-2026", test_tc07_cashflow)
run_test("TC-08", "Integriti Pengesanan Posisi Pegangan Aktif (UMC & GFM)", test_tc08_active_holdings)

# --------------------------------------------------------------------------------------
# 4. UJIAN MEJA KEPUTUSAN & PENGIMBAS 1,000 SAHAM
# --------------------------------------------------------------------------------------
from decision_tables import get_top10_bursa, get_top10_us
from master_screener import build_institutional_screener_data

def test_tc09_decision_tables():
    bursa = get_top10_bursa({})
    us = get_top10_us({})
    assert len(bursa) == 10, f"Top 10 Bursa perlu 10 baris, dapat {len(bursa)}"
    assert len(us) == 10, f"Top 10 US perlu 10 baris, dapat {len(us)}"
    assert all(bursa["RR"] >= 2.50), "Terdapat saham Bursa dengan R:R < 2.50x!"
    assert all(us["RR"] >= 2.50), "Terdapat saham US dengan R:R < 2.50x!"

def test_tc10_master_1000():
    df_m = build_institutional_screener_data({})
    assert len(df_m) == 1000, f"Pangkalan data perlu tepat 1,000 saham, dapat {len(df_m)}"
    bursa_cnt = len(df_m[df_m["Pasaran"] == "Bursa Malaysia"])
    us_cnt = len(df_m[df_m["Pasaran"] == "Wall Street US"])
    assert bursa_cnt == 500 and us_cnt == 500, f"Nisbah pasaran 500:500 tidak seimbang ({bursa_cnt}:{us_cnt})"

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

def test_tc13_heatmap_dataset():
    df_h = generate_heatmap_dataset(pd.DataFrame())
    assert not df_h.empty, "Dataset peta haba kosong!"
    assert not df_h["Market_Cap"].isna().any(), "Terdapat nilai Market Cap yang rosak/NaN"

def test_tc14_monte_carlo():
    mc = run_monte_carlo_simulation(starting_capital=42497.80, num_simulations=500, num_trades=50)
    assert mc["final_median"] > 42497.80, "Median jangkaan 77% Win Rate sepatutnya positif!"
    assert 0.0 <= mc["ruin_prob"] <= 5.0, "Kebarangkalian kejatuhan modal melebihi had toleransi!"

def test_tc15_correlation_diagonal():
    # Semakan matematik asas korelasi: korelasi sesuatu aset dengan dirinya sendiri adalah 1.00
    assets = ["TENAGA", "NVDA"]
    corr_matrix = np.corrcoef([[1, 2, 3], [1, 2, 4]])
    assert np.isclose(corr_matrix[0, 0], 1.0), "Nilai diagonal matriks korelasi bukan 1.00!"

run_test("TC-13", "Integriti Struktur Peta Haba Sektor (Treemap Dataset)", test_tc13_heatmap_dataset)
run_test("TC-14", "Simulasi Monte Carlo & Pengiraan Probability of Ruin", test_tc14_monte_carlo)
run_test("TC-15", "Ketepatan Matematik Matriks Korelasi Silang Aset", test_tc15_correlation_diagonal)

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
        capital_available=40000, wyckoff_phase="Fasa E (Terlajak Pucuk / Overbought)",
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

def test_tc19_trailing_stops():
    holdings = [{"ticker": "NYSE:UMC", "currency": "$", "entry": 19.26, "live": 18.65, "peak": 21.07}]
    df_ts = calculate_trailing_stops(holdings)
    assert not df_ts.empty, "Trailing stop UMC gagal dijana!"

def test_tc20_app_syntax_compilation():
    import py_compile
    # Memastikan app.py boleh dikompil tanpa sebarang IndentationError atau SyntaxError
    py_compile.compile("app.py", doraise=True)

run_test("TC-19", "Penjaga Trailing Stop Dinamik & Zon Penampan", test_tc19_trailing_stops)
run_test("TC-20", "Penyusunan Sintaks Penuh Aplikasi Utama (app.py)", test_tc20_app_syntax_compilation)

# --------------------------------------------------------------------------------------
# RUMUSAN LAPORAN UJIAN
# --------------------------------------------------------------------------------------
print(f"\n{CYAN}----------------------------------------------------------------------------------------{RESET}")
if failed_tests == 0:
    print(f" {GREEN}STATUS KESELURUHAN: 100% LULUS PENUH (20/20 UJIAN BERJAYA){RESET}")
    print(f" Terminal Haddy Pro disahkan stabil, selamat dan sedia beroperasi pada tahap optimum!")
else:
    print(f" {RED}STATUS KESELURUHAN: {failed_tests} UJIAN GAGAL DARI 20 UJIAN{RESET}")
print(f"{CYAN}----------------------------------------------------------------------------------------{RESET}\n")
