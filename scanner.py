import yfinance as yf
import pandas as pd
import streamlit as st
import time
import requests
import numpy as np
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

# List stocks (Tetap original)
stocks = ["GOTO.JK", "BUKA.JK", "EMTK.JK", "INET.JK", "MLPT.JK", "DCII.JK", "ATIC.JK", "GLVA.JK", "MTDL.JK", "WIFI.JK", "LUCK.JK", "AWAN.JK", "CHIP.JK", "ELIT.JK", "CYBR.JK", "GALB.JK", "IRSX.JK", "LUCY.JK", "METI.JK", "NINE.JK",
    "BBCA.JK", "BBRI.JK", "BMRI.JK", "BBNI.JK", "ARTO.JK", "BRIS.JK", "BBTN.JK", "BDMN.JK", "PNBN.JK", "BJBR.JK", "BJTM.JK", "BNLI.JK", "BVIC.JK", "MEGA.JK", "BNGA.JK", "ADMF.JK", "CFIN.JK", "BBYB.JK", "BINA.JK", "DNAR.JK", "AGRO.JK", "BABP.JK", "BACA.JK", "BAEK.JK", "BCIC.JK", "BEKS.JK", "BGTG.JK", "MAYA.JK", "MCOR.JK", "NISP.JK", "NOBU.JK", "PNBS.JK", "SDRA.JK", "VICIC.JK", "AMAR.JK", "MASB.JK",
    "ADRO.JK", "PTBA.JK", "ITMG.JK", "HRUM.JK", "INDY.JK", "MEDC.JK", "ENRG.JK", "PGAS.JK", "AKRA.JK", "DOID.JK", "BUMI.JK", "RMKE.JK", "ELSA.JK", "ADMR.JK", "MBMA.JK", "KKGI.JK", "GEMS.JK", "SGER.JK", "BYAN.JK", "RAJA.JK", "APEX.JK", "ARTI.JK", "BIPI.JK", "BOSS.JK", "DEWA.JK", "GTSI.JK", "IATA.JK", "INPS.JK", "JSKY.JK", "KOPI.JK", "MBSS.JK", "MCOL.JK", "MITI.JK", "MTFN.JK", "MYOH.JK", "PKPK.JK", "RUIS.JK", "SURE.JK", "WOWS.JK", "TEBE.JK",
    "UNVR.JK", "ICBP.JK", "INDF.JK", "AMRT.JK", "MIDI.JK", "CPIN.JK", "JPFA.JK", "MAIN.JK", "MYOR.JK", "GGRM.JK", "HMSP.JK", "DSNG.JK", "AALI.JK", "LSIP.JK", "TAPG.JK", "STAA.JK", "TBLA.JK", "CLEO.JK", "ROTI.JK", "WMPP.JK", "ADES.JK", "AISA.JK", "ALTO.JK", "ANDI.JK", "BEEF.JK", "CAMP.JK", "CEKA.JK", "DLTA.JK", "FOOD.JK", "GOOD.JK", "HOKI.JK", "IKAN.JK", "KEJU.JK", "MLBI.JK", "PCAR.JK", "PSDN.JK", "SKBM.JK", "SKLT.JK", "STTP.JK", "ULTJ.JK",
    "MAPI.JK", "ACES.JK", "ERAA.JK", "ASII.JK", "SMSM.JK", "IMAS.JK", "GJTL.JK", "MNCN.JK", "SCMA.JK", "RALS.JK", "LPPF.JK", "PNLF.JK", "MAPA.JK", "AUTO.JK", "MASA.JK", "PANI.JK", "BIRD.JK", "FILM.JK", "FORZ.JK", "GLOB.JK", "HERO.JK", "HOME.JK", "HOTL.JK", "ICON.JK", "KBLV.JK", "LPPS.JK", "MICE.JK", "MPPA.JK", "MSIN.JK", "PBSA.JK", "RICY.JK", "TARA.JK", "UNIT.JK", "WOOD.JK", "ZINC.JK", "TOSK.JK", "VIVA.JK", "KDTN.JK", "BELI.JK",
    "KLBF.JK", "MIKA.JK", "HEAL.JK", "SILO.JK", "PRDA.JK", "SAME.JK", "PEHA.JK", "PYFA.JK", "IRRA.JK", "KAEF.JK", "INAF.JK", "DGNS.JK", "BMHS.JK", "TSPC.JK", "DVLA.JK", "MERK.JK", "SIDO.JK", "SOHO.JK", "PRIM.JK", "RSGK.JK",
    "TLKM.JK", "ISAT.JK", "EXCL.JK", "JSMR.JK", "BREN.JK", "POWR.JK", "KEEN.JK", "ADHI.JK", "PTPP.JK", "WIKA.JK", "WKTK.JK", "META.JK", "TOWR.JK", "TBIG.JK", "PGEO.JK", "BRPT.JK", "FREN.JK", "LINK.JK", "BALI.JK", "BUKK.JK", "CASS.JK", "CENT.JK", "CMNP.JK", "GAMA.JK", "GHON.JK", "GOLD.JK", "IBST.JK", "IPCC.JK", "JKON.JK", "KARE.JK", "LAPD.JK", "MANT.JK", "NRCA.JK", "OASA.JK", "PBSA.JK", "PORT.JK", "SSIA.JK", "SUPR.JK", "TELE.JK", "TOPS.JK",
    "UNTR.JK", "ARNA.JK", "ASGR.JK", "IMPC.JK", "MLIA.JK", "HEXA.JK", "GMFI.JK", "BPTR.JK", "ABMM.JK", "WOOD.JK", "KMTR.JK", "SPTO.JK", "VOKS.JK", "AMFG.JK", "APLI.JK", "BRAM.JK", "DYAN.JK", "IKAI.JK", "JECC.JK", "KBLI.JK", "KBLM.JK", "LION.JK", "LMSH.JK", "PICO.JK", "PRAS.JK", "SCCO.JK", "SIPD.JK", "SULI.JK", "TALF.JK", "TIRT.JK",
    "TPIA.JK", "BRPT.JK", "ANTM.JK", "INCO.JK", "TINS.JK", "MDKA.JK", "SMGR.JK", "INTP.JK", "MBMA.JK", "NCKL.JK", "ADMG.JK", "AVIA.JK", "ESSA.JK", "SRTG.JK", "AGII.JK", "ALDO.JK", "ALKA.JK", "ALMI.JK", "BAJA.JK", "BTON.JK", "CTBN.JK", "DPNS.JK", "EKAD.JK", "ETWA.JK", "GDST.JK", "IAAS.JK", "IGAR.JK", "INAI.JK", "INCI.JK", "ISSP.JK", "KBRI.JK", "KDSI.JK", "KIAS.JK", "NIKL.JK", "PANI.JK", "SMDR.JK", "SMMT.JK", "SPMA.JK", "TOTO.JK",
    "BSDE.JK", "PWON.JK", "SMRA.JK", "CTRA.JK", "ASRI.JK", "MKPI.JK", "DILD.JK", "LPCK.JK", "LPKR.JK", "DMAS.JK", "BEST.JK", "KIJA.JK", "MTLA.JK", "JRPT.JK", "ADCP.JK", "AMAN.JK", "APLN.JK", "ARMY.JK", "BAPA.JK", "BAPI.JK", "BBSS.JK", "BCIP.JK", "BIKA.JK", "BIPP.JK", "BKDP.JK", "BKSL.JK", "COCO.JK", "CPRI.JK", "CSIS.JK", "DUTI.JK", "ELTY.JK", "EMDE.JK", "FMII.JK", "FORZ.JK", "GAMA.JK", "GMTD.JK", "GPRA.JK", "GWSA.JK", "HDIT.JK", "INPP.JK",
    "BIRD.JK", "ASSA.JK", "SMDR.JK", "TMAS.JK", "GIAA.JK", "NELY.JK", "BLUE.JK", "PSSI.JK", "ELPI.JK", "HUMI.JK", "JAYA.JK", "PORT.JK", "SDMU.JK", "AKSI.JK", "BESS.JK", "BPTR.JK", "COAL.JK", "GTSI.JK", "HELI.JK", "HOPE.JK", "IPCC.JK", "KAYU.JK", "MIRA.JK", "PBSA.JK", "SAFE.JK", "SAPX.JK", "SHIP.JK", "TNCA.JK", "TRUK.JK"]

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Scanner Settings")
    scanner_mode = st.radio("Pilih Mode Scanner:", ["Standard Accum", "Bottom Radar (Z-Score)"])
    
    st.divider()
    min_turnover = st.number_input("Min Transaksi (Miliar Rp)", value=1.0, step=0.5) * 1_000_000_000
    rvol_threshold = st.slider("Min Relative Volume", 1.0, 5.0, 1.2)
    atr_period = st.number_input("ATR Period (for TP/SL)", value=14)
    st.info("Scanner refresh otomatis tiap 180 detik.")

@st.cache_data(ttl=60)
def fetch_data(stock_list):
    return yf.download(stock_list, period="6mo", group_by='ticker', progress=False)

# --- MAIN LOGIC ---
try:
    all_data = fetch_data(stocks)
    results = []

    for stock in stocks:
        try:
            df = all_data[stock].copy().dropna()
            if len(df) < 30: continue
            
            # --- NET FLOW / VOLUME FORCE (Konfirmasi Akum/Sell) ---
            # Mengukur Net Volume: Jika Close naik, volume dianggap '+', jika turun '-', lalu di-rolling
            df['NetVol'] = np.where(df['Close'] > df['Close'].shift(1), df['Volume'], -df['Volume'])
            df['NetVol_5D'] = df['NetVol'].rolling(5).sum() # Net Flow 5 hari terakhir
            
            # --- Z-SCORE (Bottom Radar) ---
            df['Mean_20'] = df['Close'].rolling(20).mean()
            df['Std_20'] = df['Close'].rolling(20).std()
            df['Z_Score'] = (df['Close'] - df['Mean_20']) / df['Std_20']
            
            # --- BASIC INDICATORS & ATR ---
            df["AvgVolume"] = df["Volume"].rolling(20).mean()
            df["RelVolume"] = df["Volume"] / df["AvgVolume"]
            df["High20"] = df["High"].rolling(20).max()
            df["Low20"] = df["Low"].rolling(20).min()
            df["ROC"] = df["Close"].pct_change(5)
            
            # ATR Calc
            tr = pd.concat([df['High']-df['Low'], abs(df['High']-df['Close'].shift()), abs(df['Low']-df['Close'].shift())], axis=1).max(axis=1)
            df['ATR'] = tr.rolling(atr_period).mean()
            
            latest = df.iloc[-1]
            turnover = latest["Close"] * latest["Volume"]
            
            if turnover < min_turnover: continue
            
            # --- LOGIC SIGNAL SELL (Bandar Jualan) ---
            # Kriteria Sell: Harga tembus Low 20 hari ATAU Harga turun tapi Net Flow negatif gede
            is_selling = "NORMAL"
            if latest["Close"] <= df["Low20"].iloc[-2] or (latest["Close"] < latest["Open"] and latest["NetVol_5D"] < 0):
                is_selling = "DISTRIBUTION 📉"

            # --- MODE SELECTION LOGIC ---
            score = 0
            entry = "WAIT"
            
            if scanner_mode == "Standard Accum":
                if latest["RelVolume"] > rvol_threshold: score += 1
                if latest["Close"] > latest["Open"]: score += 1
                if latest["Close"] >= latest["High20"]: score += 1
                if latest["NetVol_5D"] > 0: score += 1 # Tambahan Konfirmasi Net Volume
                if score >= 3: entry = "BUY 🔥"
                elif score == 2: entry = "WATCH 👀"
            
            else: # Bottom Radar Mode
                # Syarat Bottom: Z-Score rendah (oversold) + Ada perlawanan (RelVol naik atau NetVol mulai +)
                if latest["Z_Score"] < -2.0: score += 2
                if latest["NetVol"] > 0: score += 1
                if latest["RelVolume"] > 1.0: score += 1
                if score >= 3: entry = "BOTTOMING 🛡️"
                elif score == 2: entry = "OVERSOLD ❄️"

            # TP/SL ATR
            tp_level = latest["Close"] + (2 * latest["ATR"])
            sl_level = latest["Close"] - (1.5 * latest["ATR"])
            
            if turnover > 50_000_000_000: impact = "HIGH ✅"
            elif turnover > 10_000_000_000: impact = "MEDIUM ⚠️"
            else: impact = "LOW 🔴"

            results.append({
                "Ticker": stock, "Price": int(latest["Close"]),
                "Z-Score": round(latest["Z_Score"], 2),
                "Net Flow": "Accum" if latest["NetVol_5D"] > 0 else "Sell",
                "ROC 5D (%)": round(latest["ROC"] * 100, 2),
                "R-Vol": round(latest["RelVolume"], 2),
                "Turnover (M)": round(turnover / 1_000_000_000, 2),
                "Impact": impact,
                "Status": is_selling, # Kolom baru buat liat jualan
                "TP (ATR)": int(tp_level), "SL (ATR)": int(sl_level),
                "Score": score, "Signal": entry
            })
        except: continue

    df_final = pd.DataFrame(results)

    if not df_final.empty:
        df_final = df_final.sort_values(by="Score", ascending=False)
        c1, c2, c3 = st.columns(3)
        c1.metric("Mode Active", scanner_mode)
        c2.metric("Saham Lolos Filter", len(df_final))
        
        # Filter BUY/BOTTOMING buat Notif
        buy_signals = df_final[(df_final["Signal"].str.contains("BUY|BOTTOMING"))]
        c3.metric("Signal Alert", len(buy_signals))

        # --- TELEGRAM LOGIC ---
        if 'last_sent_tickers' not in st.session_state:
            st.session_state.last_sent_tickers = set()

        if not buy_signals.empty:
            st.error(f"🚨 ALERT {scanner_mode.upper()} DETECTED!")
            st.table(buy_signals)
            
            current_buy_tickers = set(buy_signals['Ticker'].tolist())
            new_to_notify = current_buy_tickers - st.session_state.last_sent_tickers

            if new_to_notify:
                msg = f"🛰️ *[{scanner_mode}] Alert ({datetime.now().strftime('%H:%M')})*\n"
                msg += "----------------------------\n"
                for t in new_to_notify:
                    row = buy_signals[buy_signals['Ticker'] == t].iloc[0]
                    msg += f"• *{row['Ticker']}* | P: {row['Price']}\n"
                    msg += f"  📊 Z-Score: {row['Z-Score']} | Flow: {row['Net Flow']}\n"
                    msg += f"  🎯 TP: {row['TP (ATR)']} | 🛑 SL: {row['SL (ATR)']}\n"
                    msg += f"  ⚠️ Status: {row['Status']}\n\n"
                send_telegram(msg)
                st.session_state.last_sent_tickers.update(new_to_notify)
            
            st.session_state.last_sent_tickers = st.session_state.last_sent_tickers.intersection(current_buy_tickers)
        else:
            st.session_state.last_sent_tickers = set()

        st.subheader("📊 Full Market Radar Results")
        st.dataframe(df_final, use_container_width=True)
    else:
        st.warning("Belum ada saham yang masuk kriteria.")

except Exception as e:
    st.error(f"Error: {e}")

# --- AUTO REFRESH ---
st.caption(f"Last update: {datetime.now().strftime('%H:%M:%S')}")
time.sleep(180)
st.rerun()
