"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL ENJIN KEWANGAN HOLISTIK & PENGURUSAN LIABILITI (WEALTH & DEBT ENGINE)
Menghubungkan 12 Teras Liabiliti, Akaun Bank, KWSP, Zakat & Jambatan Pasaran Saham
========================================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Pemetaan GID 12 Tab Liabiliti & Kewangan Peribadi
DEBT_WEALTH_GIDS = {
    "Pengurusan_Hutang": 132297070,
    "Profil_Kredit_Experian": 7004529,
    "akaun bank millx": 116986296,
    "Kad_Kredit_RHB": 1928302918,
    "Perjanjian Sewa Beli": 144766196,
    "PTPTN": 721185977,
    "Penyelenggaraan_Castana": 1163122475,
    "KWSP": 574881366,
    "Taksiran_Zakat": 1610247390,
    "Panduan_Syariah": 1677076971,
    "Pinjaman_Peribadi_CIMB": 82870378,
    "AKPK_DMP": 1522726426
}

def get_holistic_balance_sheet(stock_portfolio_val=55945.32, cash_reserve=18500.00):
    """
    Menjana Penyata Imbangan Lengkap (Aset vs Liabiliti)
    """
    # 1. Aset Semasa & Pelaburan
    assets = [
        {"Kategori": "Pelaburan Saham (Bursa & US)", "Institusi": "Moomoo Universal (8702)", "Nilai_MYR": stock_portfolio_val, "Likuiditi": "Tinggi"},
        {"Kategori": "Simpanan Tunai & Bank", "Institusi": "Maybank Islamic / Millx Bank", "Nilai_MYR": cash_reserve, "Likuiditi": "Serta-merta"},
        {"Kategori": "Simpanan Syariah", "Institusi": "Lembaga Tabung Haji", "Nilai_MYR": 15400.00, "Likuiditi": "Tinggi"},
        {"Kategori": "Amanah Saham", "Institusi": "ASNB (ASM / ASB)", "Nilai_MYR": 12850.00, "Likuiditi": "Tinggi"},
        {"Kategori": "Dana Persaraan", "Institusi": "KWSP (Simpanan Shariah)", "Nilai_MYR": 168400.00, "Likuiditi": "Terkunci"},
        {"Kategori": "Aset Hartanah Kediaman", "Institusi": "Kediaman Castana", "Nilai_MYR": 480000.00, "Likuiditi": "Rendah"},
        {"Kategori": "Kenderaan Peribadi", "Institusi": "Perodua Alza 1.5X & Bezza 1.0", "Nilai_MYR": 85000.00, "Likuiditi": "Sederhana"}
    ]
    df_assets = pd.DataFrame(assets)
    total_assets = df_assets["Nilai_MYR"].sum()

    # 2. Liabiliti & Pinjaman Portfolio (CCRIS BNM)
    liabilities = [
        {"No": 1, "Fasiliti": "Pinjaman Perumahan (Castana)", "Institusi": "BSN (Bersama)", "Baki_Semasa": 408048.00, "Had_Asal": 388739.00, "Ansuran_Bulanan": 1400.00, "Kadar": "4.10%", "Status": "DMP AKPK", "Jenis": "Properties"},
        {"No": 2, "Fasiliti": "Sewa Beli Kenderaan", "Institusi": "Perodua Bezza (Maybank)", "Baki_Semasa": 13766.64, "Had_Asal": 32900.00, "Ansuran_Bulanan": 396.00, "Kadar": "6.69%", "Status": "Aktif", "Jenis": "Motor V"},
        {"No": 3, "Fasiliti": "Kad Kredit (Rewards)", "Institusi": "RHB Islamic (Card-i)", "Baki_Semasa": 4682.05, "Had_Asal": 19000.00, "Ansuran_Bulanan": 50.00, "Kadar": "7.00%", "Status": "DMP AKPK", "Jenis": "Clean"},
        {"No": 4, "Fasiliti": "Kad Kredit (Cashback)", "Institusi": "RHB Islamic (Berkongsi)", "Baki_Semasa": 13638.26, "Had_Asal": 19000.00, "Ansuran_Bulanan": 100.00, "Kadar": "7.00%", "Status": "DMP AKPK", "Jenis": "Clean"},
        {"No": 5, "Fasiliti": "Pinjaman Peribadi", "Institusi": "CIMB Cash Plus", "Baki_Semasa": 94013.13, "Had_Asal": 100000.00, "Ansuran_Bulanan": 950.00, "Kadar": "7.00%", "Status": "DMP AKPK", "Jenis": "Clean"},
        {"No": 6, "Fasiliti": "Sewa Beli Kenderaan", "Institusi": "Perodua Alza (Hong Leong)", "Baki_Semasa": 61123.74, "Had_Asal": 63000.00, "Ansuran_Bulanan": 704.00, "Kadar": "2.29%", "Status": "Aktif", "Jenis": "Motor V"},
        {"No": 7, "Fasiliti": "Pinjaman Pendidikan", "Institusi": "PTPTN (Ujrah 1%)", "Baki_Semasa": 18450.00, "Had_Asal": 25000.00, "Ansuran_Bulanan": 150.00, "Kadar": "1.00%", "Status": "Aktif", "Jenis": "Pendidikan"}
    ]
    df_liabilities = pd.DataFrame(liabilities)
    total_liabilities = df_liabilities["Baki_Semasa"].sum()
    total_monthly_commitment = df_liabilities["Ansuran_Bulanan"].sum()

    # 3. Nilai Bersih (Net Worth)
    net_worth = total_assets - total_liabilities
    solvency_ratio = (total_assets / total_liabilities) if total_liabilities > 0 else 0.0

    return {
        "df_assets": df_assets,
        "df_liabilities": df_liabilities,
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "total_monthly_commitment": total_monthly_commitment,
        "net_worth": net_worth,
        "solvency_ratio": solvency_ratio,
        "dmp_monthly_savings": 981.00
    }

def get_syariah_reminders():
    """Koleksi Nas Al-Quran & Hadis Sahih Pengurusan Kewangan"""
    return [
        {
            "Surah_Hadis": "Surah Al-Baqarah : Ayat 275",
            "Maksud": "Allah menghalalkan jual beli dan mengharamkan riba.",
            "Tafsiran": "Wajib mengelakkan pinjaman berasaskan riba. Utamakan pembiayaan patuh Syariah (AITAB, Murabahah)."
        },
        {
            "Surah_Hadis": "HR At-Tirmidhi (Sahih)",
            "Maksud": "Jiwa seorang mukmin tergantung dengan hutangnya sehinggalah hutang itu dilunaskan.",
            "Tafsiran": "Amanah melunaskan hutang adalah kewajipan fardu yang mengikat rohani pelabur."
        },
        {
            "Surah_Hadis": "HR Al-Bukhari (Sahih)",
            "Maksud": "Barangsiapa meminjam harta orang dengan niat membayarnya, Allah akan menolong melunaskannya.",
            "Tafsiran": "Niat yang tulus dan disiplin pembayaran bulanan mengundang pertolongan dan keberkatan Ilahi."
        },
        {
            "Surah_Hadis": "HR Al-Bukhari (Doa Perlindungan)",
            "Maksud": "Ya Allah, aku berlindung kepada-Mu daripada kesedihan, kelemahan, kemalasan, dan belenggu hutang.",
            "Tafsiran": "Amalkan doa harian bagi melindungi minda daripada tekanan liabiliti melampau."
        }
    ]
