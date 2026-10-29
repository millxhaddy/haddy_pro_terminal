"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL FASAA 1: ENJIN KOMPUTASI FLUENT & STATUS PASARAN DWIBENUA (MODERN CORE)
========================================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime
import pytz

def get_dual_market_status():
    """
    Mengira status waktu operasi semasa bagi Bursa Malaysia & Wall Street US
    lengkap dengan zon masa tempatan masing-masing (MYT & US Eastern).
    """
    if pytz:
        myt_zone = pytz.timezone("Asia/Kuala_Lumpur")
        est_zone = pytz.timezone("America/New_York")
        now_myt = datetime.now(myt_zone)
        now_est = datetime.now(est_zone)
    else:
        now_myt = datetime.now(timezone(timedelta(hours=8)))
        now_est = datetime.now(timezone(timedelta(hours=-5)))
    
    # 1. Status Bursa Malaysia (Isnin - Jumaat)
    weekday_my = now_myt.weekday()  # 0: Isnin, 4: Jumaat, 5-6: Hujung Minggu
    time_my = now_myt.hour * 100 + now_myt.minute
    
    if weekday_my >= 5:
        bursa_status = "🔴 HUJUNG MINGGU (TUTUP)"
        bursa_color = "#FF5252"
    elif 900 <= time_my < 1230:
        bursa_status = "🟢 SESI PAGI (DIBUKA)"
        bursa_color = "#00E676"
    elif 1230 <= time_my < 1430:
        bursa_status = "🟡 REHAT TENGAH HARI"
        bursa_color = "#FFBB28"
    elif 1430 <= time_my < 1700:
        bursa_status = "🟢 SESI PETANG (DIBUKA)"
        bursa_color = "#00E676"
    else:
        bursa_status = "⚪ LUAR SESI (TUTUP)"
        bursa_color = "#8E9AAF"

    # 2. Status Wall Street US (Isnin - Jumaat)
    weekday_us = now_est.weekday()
    time_us = now_est.hour * 100 + now_est.minute
    
    if weekday_us >= 5:
        us_status = "🔴 HUJUNG MINGGU (TUTUP)"
        us_color = "#FF5252"
    elif 400 <= time_us < 930:
        us_status = "🟡 PRA-PASARAN (PRE-MARKET)"
        us_color = "#FFBB28"
    elif 930 <= time_us < 1600:
        us_status = "🟢 SESI UTAMA (DIBUKA)"
        us_color = "#00E676"
    elif 1600 <= time_us < 2000:
        us_status = "🔵 SELEPAS WAKTU (AFTER-HOURS)"
        us_color = "#29B6F6"
    else:
        us_status = "⚪ LUAR SESI (TUTUP)"
        us_color = "#8E9AAF"

    return {
        "bursa": {
            "status": bursa_status,
            "color": bursa_color,
            "time_str": now_myt.strftime("%d-%m-%Y %H:%M:%S MYT")
        },
        "us": {
            "status": us_status,
            "color": us_color,
            "time_str": now_est.strftime("%d-%m-%Y %H:%M:%S EST")
        }
    }

def compute_fast_indicators(df_ohlcv: pd.DataFrame) -> pd.DataFrame:
    """
    Mengira indikator teknikal pantas (RSI, EMA 20/50, ATR) menggunakan pandas_ta.
    Jika pandas_ta tiada, menggunakan fallback NumPy pantas.
    """
    if df_ohlcv.empty or len(df_ohlcv) < 14:
        return df_ohlcv
        
    df = df_ohlcv.copy()
    try:
        import pandas_ta as ta
        df["EMA20"] = ta.ema(df["Close"], length=20)
        df["EMA50"] = ta.ema(df["Close"], length=50)
        df["RSI"] = ta.rsi(df["Close"], length=14)
        df["ATR"] = ta.atr(df["High"], df["Low"], df["Close"], length=14)
    except Exception:
        # Fallback pantas
        df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
        df["EMA50"] = df["Close"].ewm(span=50, adjust=False).mean()
        delta = df["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss.replace(0, np.nan)
        df["RSI"] = 100 - (100 / (1 + rs))
        df["RSI"] = df["RSI"].fillna(50.0)
        df["ATR"] = (df["High"] - df["Low"]).rolling(14).mean()
        
    return df