import yfinance as yf
import pandas as pd
import streamlit as st
import time
import requests
from datetime import datetime

# --- CONFIG TELEGRAM ---
TOKEN = "8641113824:AAGWK4MYSgr9ilS2RoDS9fMFuRheJgJbQo8"
CHAT_ID = "1186394676"

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID, 
            "text": message, 
            "parse_mode": "Markdown"
        }
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        st.error(f"Gagal kirim Telegram: {e}")

# --- CONFIG & SETUP ---
st.set_page_config(layout="wide", page_title="Quant Scanner Indo")
st.title("🔥 Ultimate Quant Scanner - IHSG Edition")

stocks = [
    "INET.JK","EXCL.JK","DKHH.JK","BNBR.JK","AUTO.JK","UNVR.JK","ICBP.JK","INDF.JK",
    "PGAS.JK","MEDC.JK","ADRO.JK","ANTM.JK","INCO.JK","MDKA.JK","TINS.JK","SMGR.JK",
    "INTP.JK","CPIN.JK","ENRG.JK","ARCI.JK","BIPI.JK","PTRO.JK","BRMS.JK","EMAS.JK",
    "JPFA.JK","ERAA.JK","MAPI.JK","BELL.JK","GOTO.JK","BUKA.JK",
    "ESSA.JK","DOOH.JK","LSIP.JK","BUMI.JK","MINA.JK","KLBF.JK","TBIG.JK","TOWR.JK","MANG.JK","IOTF.JK",
    "BUVA.JK","PTPP.JK","YELO.JK","APLN.JK","OILS.JK","AYLS.JK","KUAS.JK","NASI.JK","GIAA.JK","RLCO.JK",
]

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Scanner Settings")
    min_turnover = st.number_input("Min Transaksi (Miliar Rp)", value=1.0, step=0.5) * 1_000_000_000
    rvol_threshold = st.slider("Min Relative Volume", 1.0, 5.0, 1.2)
    st.info("Scanner refresh otomatis tiap 60 detik.")

@st.cache_data(ttl=60)
def fetch_data(stock_list):
    return yf.download(stock_list, period="3mo", group_by='ticker', progress=False)

# --- MAIN LOGIC ---
try:
    all_data = fetch_data(stocks)
    results = []

    for stock in stocks:
        try:
            df = all_data[stock].copy().dropna()
            if len(df) < 20: continue
            df["AvgVolume"] = df["Volume"].rolling(20).mean()
            df["RelVolume"] = df["Volume"] / df["AvgVolume"]
            df["High20"] = df["High"].rolling(20).max()
            df["ROC"] = df["Close"].pct_change(5)
            latest = df.iloc[-1]
            turnover = latest["Close"] * latest["Volume"]
            if turnover < min_turnover: continue
            score = 0
            if latest["RelVolume"] > rvol_threshold: score += 1
            if latest["Close"] > latest["Open"]: score += 1
            if latest["Close"] >= latest["High20"]: score += 1
            if latest["ROC"] > 0: score += 1
            entry = "WAIT"
            if score >= 3: entry = "BUY 🔥"
            elif score == 2: entry = "WATCH 👀"
            results.append({
                "Ticker": stock, "Price": int(latest["Close"]),
                "ROC 5D (%)": round(latest["ROC"] * 100, 2),
                "R-Vol": round(latest["RelVolume"], 2),
                "Turnover (M)": round(turnover / 1_000_000_000, 2),
                "Score": score, "Signal": entry
            })
        except: continue

    df_final = pd.DataFrame(results)

    if not df_final.empty:
        df_final = df_final.sort_values(by="Score", ascending=False)
        c1, c2, c3 = st.columns(3)
        c1.metric("Saham Di-scan", len(stocks))
        c2.metric("Lolos Filter", len(df_final))
        buy_signals = df_final[df_final["Score"] >= 3]
        c3.metric("Signal BUY", len(buy_signals))

        # --- TELEGRAM LOGIC (STRICT ANTI-SPAM) ---
        if not buy_signals.empty:
            st.error("🚨 SIGNAL KUAT TERDETEKSI!")
            st.table(buy_signals)
            
            # Inisialisasi memory di session_state
            if 'last_sent_tickers' not in st.session_state:
                st.session_state.last_sent_tickers = set()

            current_buy_tickers = set(buy_signals['Ticker'].tolist())
            # Cari saham yang BELUM pernah dikirim notifnya
            new_to_notify = current_buy_tickers - st.session_state.last_sent_tickers

            if new_to_notify:
                msg = f"🚀 *Quant Alert Baru ({datetime.now().strftime('%H:%M')})*\n"
                for t in new_to_notify:
                    row = buy_signals[buy_signals['Ticker'] == t].iloc[0]
                    msg += f"• *{row['Ticker']}*: Price {row['Price']} (Score: {row['Score']})\n"
                
                send_telegram(msg)
                # Update memory: sekarang ticker ini sudah dianggap "pernah dikirim"
                st.session_state.last_sent_tickers.update(new_to_notify)
            
            # Bersihkan ticker lama yang sudah gak BUY dari memory (biar bisa bunyi lagi nanti)
            st.session_state.last_sent_tickers = st.session_state.last_sent_tickers.intersection(current_buy_tickers)
        else:
            st.session_state.last_sent_tickers = set()

        st.subheader("📊 Full Scanner Results")
        st.dataframe(df_final, use_container_width=True)
    else:
        st.warning("Belum ada saham yang masuk kriteria.")

except Exception as e:
    st.error(f"Error: {e}")

# --- AUTO REFRESH ---
st.caption(f"Last update: {datetime.now().strftime('%H:%M:%S')}")
time.sleep(60)
st.rerun()
