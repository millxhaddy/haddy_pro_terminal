"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL FASA 3: PIPELINE PEMBERSIHAN DATA & PENYERAGAMAN SKEMA (DATA CLEANER)
========================================================================================
"""

import pandas as pd
import numpy as np
import re

def clean_currency(val):
    """Menukar teks berformat wang (cth: 'RM 12.75', '$141.20', 'RM (1,958.00)') kepada nombor float."""
    if pd.isna(val):
        return 0.0
    val_str = str(val).strip()
    if not val_str or val_str in ["-", "N/A", "nan"]:
        return 0.0
    
    # Kesan nilai negatif dalam kurungan (cth: (1,958.00))
    is_negative = "(" in val_str and ")" in val_str or val_str.startswith("-")
    
    # Buang semua aksara bukan digit/perpuluhan
    clean_str = re.sub(r"[^\d.]", "", val_str)
    try:
        num = float(clean_str)
        return -num if is_negative else num
    except:
        return 0.0

def clean_percentage(val):
    """Menukar format peratus (cth: '15.5%', '0.045') kepada nombor perpuluhan."""
    if pd.isna(val):
        return 0.0
    val_str = str(val).strip()
    if not val_str or val_str in ["-", "N/A"]:
        return 0.0
    is_negative = "-" in val_str or "(" in val_str
    clean_str = re.sub(r"[^\d.]", "", val_str)
    try:
        num = float(clean_str)
        if "%" in str(val):
            num = num / 100.0
        return -num if is_negative else num
    except:
        return 0.0

def clean_ratio(val):
    """Mengekstrak nilai nisbah gandaan R:R (cth: '2.50x' -> 2.50)."""
    if pd.isna(val):
        return 0.0
    val_str = str(val).lower().replace("x", "").strip()
    try:
        return float(re.sub(r"[^\d.]", "", val_str))
    except:
        return 0.0

def process_master_database(df: pd.DataFrame) -> pd.DataFrame:
    """Membersihkan skema 1,000 Saham Master Database."""
    if df.empty:
        return pd.DataFrame()
    
    df_clean = df.copy()
    
    # Pembersihan kod ticker (buang ruang kosong)
    if "Ticker Google" in df_clean.columns:
        df_clean["Ticker_Clean"] = df_clean["Ticker Google"].astype(str).str.strip()
    elif "Ticker" in df_clean.columns:
        df_clean["Ticker_Clean"] = df_clean["Ticker"].astype(str).str.strip()
    else:
        df_clean["Ticker_Clean"] = df_clean.iloc[:, 0].astype(str).str.strip()

    # Kenal pasti lajur harga
    price_cols = [c for c in df_clean.columns if "Harga" in c or "Price" in c]
    if price_cols:
        df_clean["Harga_Semasa"] = df_clean[price_cols[0]].apply(clean_currency)
    else:
        df_clean["Harga_Semasa"] = 0.0

    # Normalisasi pasaran (Bursa vs US)
    market_cols = [c for c in df_clean.columns if "Pasaran" in c or "Market" in c]
    if market_cols:
        df_clean["Pasaran_Kategori"] = df_clean[market_cols[0]].apply(
            lambda x: "Bursa Malaysia" if any(k in str(x).upper() for k in ["BURSA", "KLSE", "MYX"]) else "Wall Street US"
        )
    else:
        df_clean["Pasaran_Kategori"] = "Global"

    # Status Saringan (Boleh Beli vs Pantau)
    status_cols = [c for c in df_clean.columns if "Keputusan" in c or "Status" in c]
    if status_cols:
        df_clean["Status_Entri"] = df_clean[status_cols[0]].astype(str).str.strip()
    else:
        df_clean["Status_Entri"] = "Pantau"

    return df_clean

def process_decision_table(df: pd.DataFrame) -> pd.DataFrame:
    """Membersihkan jadual Meja Keputusan Harian (Top 10 Bursa & Top 10 US)."""
    if df.empty:
        return pd.DataFrame()
    
    df_clean = df.copy()
    
    # Cari lajur berkaitan
    col_map = {c: str(c).strip() for c in df_clean.columns}
    df_clean.rename(columns=col_map, inplace=True)
    
    for col in df_clean.columns:
        c_upper = col.upper()
        if "HARGA" in c_upper:
            df_clean["Harga_Numeric"] = df_clean[col].apply(clean_currency)
        elif "STOP LOSS" in c_upper or "SL" in c_upper:
            df_clean["SL_Numeric"] = df_clean[col].apply(clean_currency)
        elif "SASARAN" in c_upper or "TP" in c_upper:
            df_clean["TP_Numeric"] = df_clean[col].apply(clean_currency)
        elif "R:R" in c_upper or "NISBAH" in c_upper:
            df_clean["RR_Ratio"] = df_clean[col].apply(clean_ratio)
            
    return df_clean
