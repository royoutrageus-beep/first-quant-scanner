import yfinance as yf
import pandas as pd
import streamlit as st
import time
from datetime import datetime

# --- CONFIG & SETUP ---
st.set_page_config(layout="wide", page_title="Quant Scanner Indo")
st.title("🔥 Ultimate Quant Scanner - IHSG Edition")

# List Saham (Bisa lo tambah sesuka hati)
stocks = [
    "INET.JK","EXCL.JK","DKHH.JK","BNBR.JK","AUTO.JK","UNVR.JK","ICBP.JK","INDF.JK",
    "PGAS.JK","MEDC.JK","ADRO.JK","ANTM.JK","INCO.JK","MDKA.JK","TINS.JK","SMGR.JK",
    "INTP.JK","CPIN.JK","ENRG.JK","ARCI.JK","BIPI.JK","PTRO.JK","BRMS.JK","EMAS.JK","JPFA.JK","ERAA.JK","MAPI.JK","BELL.JK","GOTO.JK","BUKA.JK",
    "ESSA.JK","DOOH.JK","LSIP.JK","BUMI.JK","MINA.JK","KLBF.JK","TBIG.JK","TOWR.JK",
    "BUVA.JK","PTPP.JK"
]

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("⚙️ Scanner Settings")
    min_turnover = st.number_input("Min Transaksi (Miliar Rp)", value=1.0, step=0.5) * 1_000_000_000
    rvol_threshold = st.slider("Min Relative Volume", 1.0, 5.0, 1.2)
    st.info("Scanner ini otomatis refresh setiap 1 menit.")

# --- DATA FETCHING (BULK) ---
@st.cache_data(ttl=60) # Cache data selama 60 detik biar gak over-request
def fetch_data(stock_list):
    # Download semua data sekaligus (jauh lebih cepat)
    return yf.download(stock_list, period="3mo", group_by='ticker', progress=False)

try:
    all_data = fetch_data(stocks)
    results = []

    # --- PROCESSING LOOP ---
    for stock in stocks:
        try:
            # Ambil data per ticker
            df = all_data[stock].copy().dropna()
            
            if len(df) < 20: continue

            # --- INDIKATOR ---
            df["AvgVolume"] = df["Volume"].rolling(20).mean()
            df["RelVolume"] = df["Volume"] / df["AvgVolume"]
            df["High20"] = df["High"].rolling(20).max()
            df["ROC"] = df["Close"].pct_change(5) # 5 hari return
            
            latest = df.iloc[-1]
            prev = df.iloc[-2]
            
            # Hitung Nilai Transaksi (Price * Volume)
            turnover = latest["Close"] * latest["Volume"]
            
            # --- FILTER LIKUIDITAS ---
            if turnover < min_turnover: continue

            # --- SCORING LOGIC ---
            score = 0
            if latest["RelVolume"] > rvol_threshold: score += 1
            if latest["Close"] > latest["Open"]: score += 1
            if latest["Close"] >= latest["High20"]: score += 1
            if latest["ROC"] > 0: score += 1

            # --- SIGNALS ---
            entry = "WAIT"
            if score >= 3: entry = "BUY 🔥"
            elif score == 2: entry = "WATCH 👀"

            exit_signal = "HOLD"
            if latest["ROC"] < -0.02: exit_signal = "SELL ⚠️" # ROC drop > 2%

            # --- APPEND RESULTS ---
            results.append({
                "Ticker": stock,
                "Price": int(latest["Close"]),
                "ROC 5D (%)": round(latest["ROC"] * 100, 2),
                "R-Vol": round(latest["RelVolume"], 2),
                "Turnover (M)": round(turnover / 1_000_000_000, 2),
                "Score": score,
                "Signal": entry,
                "Action": exit_signal
            })

        except Exception as e:
            continue # Skip kalo ada saham yang datanya error

    # --- UI RENDERING ---
    df_final = pd.DataFrame(results)

    if not df_final.empty:
        df_final = df_final.sort_values(by="Score", ascending=False)

        # Dashboard Atas
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Saham Di-scan", len(stocks))
        with c2: st.metric("Lolos Filter", len(df_final))
        with c3: st.metric("Signal BUY", len(df_final[df_final["Score"] >= 3]))

        # Alert Section
        strong_signals = df_final[df_final["Score"] >= 3]
        if not strong_signals.empty:
            st.error("🚨 SIGNAL KUAT TERDETEKSI!")
            st.table(strong_signals)

        # Full Data Table
        st.subheader("📊 Full Market Scanner Results")
        st.dataframe(df_final, use_container_width=True)
    else:
        st.warning("Tidak ada saham yang memenuhi kriteria likuiditas/data.")

except Exception as e:
    st.error(f"Gagal narik data dari Yahoo Finance: {e}")

# --- AUTO REFRESH ---
st.caption(f"Terakhir update: {datetime.now().strftime('%H:%M:%S')}")
time.sleep(60)
st.rerun()