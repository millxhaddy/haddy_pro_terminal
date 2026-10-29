"""
HADDY PRO - TERMINAL MILLX
MODUL ENJIN KEWANGAN HOLISTIK & PENGURUSAN LIABILITI (DATA SEBENAR GOOGLE SHEETS)
"""
import pandas as pd
import numpy as np

def get_holistic_balance_sheet(stock_portfolio_val=54278.00, cash_reserve=42497.80):
    assets = [
        {"Kategori": "Pelaburan Saham (Bursa & US)", "Institusi": "Moomoo Universal (8702)", "Nilai_MYR": stock_portfolio_val, "Likuiditi": "Tinggi"},
        {"Kategori": "Baki Modal Trading Tunai", "Institusi": "Moomoo Funding Vault", "Nilai_MYR": cash_reserve, "Likuiditi": "Tinggi"},
        {"Kategori": "Simpanan Tunai Bank", "Institusi": "Maybank Islamic (Savers-i)", "Nilai_MYR": 4.24, "Likuiditi": "Serta-merta"},
        {"Kategori": "Simpanan Haji", "Institusi": "Lembaga Tabung Haji (T1)", "Nilai_MYR": 44.84, "Likuiditi": "Tinggi"},
        {"Kategori": "Amanah Saham", "Institusi": "ASNB (523.21 Unit)", "Nilai_MYR": 549.07, "Likuiditi": "Tinggi"},
        {"Kategori": "Dana Persaraan Shariah", "Institusi": "KWSP (Akaun 1, 2, 3)", "Nilai_MYR": 251831.78, "Likuiditi": "Terkunci"},
        {"Kategori": "Aset Hartanah Kediaman", "Institusi": "Kediaman Castana", "Nilai_MYR": 480000.00, "Likuiditi": "Rendah"},
        {"Kategori": "Kenderaan Peribadi", "Institusi": "Perodua Alza 1.5X & Bezza 1.0", "Nilai_MYR": 85000.00, "Likuiditi": "Sederhana"}
    ]
    df_assets = pd.DataFrame(assets)
    total_assets = df_assets["Nilai_MYR"].sum()

    liabilities = [
        {"No": 1, "Fasiliti": "Pinjaman Perumahan", "Institusi": "Pembiayaan Bersama (BSN)", "Baki_Semasa": 408048.18, "Had_Asal": 388739.00, "Ansuran_Bulanan": 1400.00, "Kadar": "4.10%", "Status": "DMP AKPK", "Jenis": "Properties"},
        {"No": 2, "Fasiliti": "Sewa Beli Kenderaan", "Institusi": "Perodua Bezza (Maybank)", "Baki_Semasa": 13766.64, "Had_Asal": 32900.00, "Ansuran_Bulanan": 396.00, "Kadar": "6.69%", "Status": "Aktif", "Jenis": "Motor V"},
        {"No": 3, "Fasiliti": "Kad Kredit (Rewards)", "Institusi": "RHB Islamic (Card-i)", "Baki_Semasa": 4682.05, "Had_Asal": 19000.00, "Ansuran_Bulanan": 50.00, "Kadar": "7.00%", "Status": "DMP AKPK", "Jenis": "Clean"},
        {"No": 4, "Fasiliti": "Kad Kredit (Cashback)", "Institusi": "RHB Islamic (Cashback)", "Baki_Semasa": 13638.26, "Had_Asal": 19000.00, "Ansuran_Bulanan": 100.00, "Kadar": "7.00%", "Status": "DMP AKPK", "Jenis": "Clean"},
        {"No": 5, "Fasiliti": "Pinjaman Peribadi", "Institusi": "CIMB Cash Plus", "Baki_Semasa": 94013.13, "Had_Asal": 100000.00, "Ansuran_Bulanan": 950.00, "Kadar": "7.00%", "Status": "DMP AKPK", "Jenis": "Clean"},
        {"No": 6, "Fasiliti": "Sewa Beli Kenderaan", "Institusi": "Perodua Alza (Hong Leong)", "Baki_Semasa": 61123.74, "Had_Asal": 63000.00, "Ansuran_Bulanan": 704.00, "Kadar": "2.29%", "Status": "Aktif", "Jenis": "Motor V"},
        {"No": 7, "Fasiliti": "Pinjaman Pendidikan", "Institusi": "PTPTN (Ujrah 1%)", "Baki_Semasa": 7229.22, "Had_Asal": 25000.00, "Ansuran_Bulanan": 150.00, "Kadar": "1.00%", "Status": "Aktif", "Jenis": "Pendidikan"}
    ]
    df_liabilities = pd.DataFrame(liabilities)
    total_liabilities = df_liabilities["Baki_Semasa"].sum()
    total_monthly_commitment = df_liabilities["Ansuran_Bulanan"].sum()

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
        "dmp_monthly_savings": 2163.29
    }
