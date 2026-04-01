import yfinance as yf
import pandas as pd
import streamlit as st
import time
import requests
import numpy as np
import pytz 
from datetime import datetime, timedelta

# --- CONFIG TELEGRAM ---
TOKEN = "8641113824:AAGWK4MYSgr9ilS2RoDS9fMFuRheJgJbQo8"
CHAT_ID = "1186394676"
jakarta_tz = pytz.timezone('Asia/Jakarta')

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        st.error(f"Gagal kirim Telegram: {e}")

# --- CONFIG & SETUP ---
st.set_page_config(layout="wide", page_title="Quant Scanner Indo")
st.title("🔥 Ultimate Quant Scanner - IHSG Edition")

# List stocks (Tetap original)
stocks = ["GOTO.JK", "BUKA.JK", "EMTK.JK", "INET.JK", "MLPT.JK", "DCII.JK", "ATIC.JK", "GLVA.JK", "MTDL.JK", "WIFI.JK", "LUCK.JK", "AWAN.JK", "CHIP.JK", "ELIT.JK", "CYBR.JK", "GALB.JK", "IRSX.JK", "LUCY.JK", "METI.JK", "NINE.JK", "BBCA.JK", "BBRI.JK", "BMRI.JK", "BBNI.JK", "ARTO.JK", "BRIS.JK", "BBTN.JK", "BDMN.JK", "PNBN.JK", 
"BJBR.JK", "BJTM.JK", "BNLI.JK", "BVIC.JK", "MEGA.JK", "BNGA.JK", "ADMF.JK", "CFIN.JK", "BBYB.JK", "BINA.JK", "DNAR.JK", "AGRO.JK", "BABP.JK", "BACA.JK", "BAEK.JK", "BCIC.JK", "BEKS.JK", "BGTG.JK", "MAYA.JK", "MCOR.JK", "NISP.JK", "NOBU.JK", "PNBS.JK", "SDRA.JK", "VICI.JK", "AMAR.JK", "MASB.JK", "ADRO.JK", "PTBA.JK", "ITMG.JK", 
"HRUM.JK", "INDY.JK", "MEDC.JK", "ENRG.JK", "PGAS.JK", "AKRA.JK", "DOID.JK", "BUMI.JK", "RMKE.JK", "ELSA.JK", "ADMR.JK", "MBMA.JK", "KKGI.JK", "GEMS.JK", "SGER.JK", "BYAN.JK", "RAJA.JK", "APEX.JK", "ARTI.JK", "BIPI.JK", "BOSS.JK", "DEWA.JK", "TOBA.JK", "IATA.JK", "INPS.JK", "JSKY.JK", "KOPI.JK", "MBSS.JK", "MCOL.JK", "MITI.JK", 
"MTFN.JK", "MYOH.JK", "PKPK.JK", "RUIS.JK", "SURE.JK", "WOWS.JK", "TEBE.JK", "UNVR.JK", "ICBP.JK", "INDF.JK", "AMRT.JK", "MIDI.JK", "CPIN.JK", "JPFA.JK", "MAIN.JK", "MYOR.JK", "GGRM.JK", "HMSP.JK", "DSNG.JK", "AALI.JK", "LSIP.JK", "TAPG.JK", "STAA.JK", "TBLA.JK", "CLEO.JK", "ROTI.JK", "WMPP.JK", "ADES.JK", "AISA.JK", "ALTO.JK", 
"ANDI.JK", "BEEF.JK", "CAMP.JK", "CEKA.JK", "DLTA.JK", "FOOD.JK", "GOOD.JK", "HOKI.JK", "IKAN.JK", "KEJU.JK", "MLBI.JK", "PCAR.JK", "PSDN.JK", "SKBM.JK", "SKLT.JK", "STTP.JK", "ULTJ.JK", "MAPI.JK", "ACES.JK", "ERAA.JK", "ASII.JK", "SMSM.JK", "IMAS.JK", "GJTL.JK", "MNCN.JK", "SCMA.JK", "RALS.JK", "LPPF.JK", "PNLF.JK", "MAPA.JK", 
"AUTO.JK", "MASA.JK", "PANI.JK", "BIRD.JK", "FILM.JK", "FORZ.JK", "GLOB.JK", "HERO.JK", "HOME.JK", "HOTL.JK", "ICON.JK", "KBLV.JK", "LPPS.JK", "MICE.JK", "MPPA.JK", "MSIN.JK", "PBSA.JK", "RICY.JK", "TARA.JK", "UNIT.JK", "WOOD.JK", "ZINC.JK", "TOSK.JK", "VIVA.JK", "KDTN.JK", "BELI.JK", "KLBF.JK", "MIKA.JK", "HEAL.JK", "SILO.JK", 
"PRDA.JK", "SAME.JK", "PEHA.JK", "PYFA.JK", "IRRA.JK", "KAEF.JK", "INAF.JK", "DGNS.JK", "BMHS.JK", "TSPC.JK", "DVLA.JK", "MERK.JK", "SIDO.JK", "SOHO.JK", "PRIM.JK", "RSGK.JK", "TLKM.JK", "ISAT.JK", "EXCL.JK", "JSMR.JK", "BREN.JK", "POWR.JK", "KEEN.JK", "ADHI.JK", "PTPP.JK", "WIKA.JK", "WKTK.JK", "META.JK", "TOWR.JK", "TBIG.JK", 
"PGEO.JK", "BRPT.JK", "FREN.JK", "LINK.JK", "BALI.JK", "BUKK.JK", "CASS.JK", "CENT.JK", "CMNP.JK", "GAMA.JK", "GHON.JK", "GOLD.JK", "IBST.JK", "IPCC.JK", "JKON.JK", "KARE.JK", "LAPD.JK", "MANT.JK", "NRCA.JK", "OASA.JK", "PBSA.JK", "PORT.JK", "SSIA.JK", "SUPR.JK", "TELE.JK", "TOPS.JK", "UNTR.JK", "ARNA.JK", "ASGR.JK", "IMPC.JK", 
"MLIA.JK", "HEXA.JK", "GMFI.JK", "BPTR.JK", "ABMM.JK", "WOOD.JK", "KMTR.JK", "SPTO.JK", "VOKS.JK", "AMFG.JK", "APLI.JK", "BRAM.JK", "DYAN.JK", "IKAI.JK", "JECC.JK", "KBLI.JK", "KBLM.JK", "LION.JK", "LMSH.JK", "PICO.JK", "PRAS.JK", "SCCO.JK", "SIPD.JK", "SULI.JK", "TALF.JK", "TIRT.JK", "TPIA.JK", "BRPT.JK", "ANTM.JK", "INCO.JK", 
"TINS.JK", "MDKA.JK", "SMGR.JK", "INTP.JK", "INKP.JK", "NCKL.JK", "ADMG.JK", "AVIA.JK", "ESSA.JK", "SRTG.JK", "AGII.JK", "ALDO.JK", "ALKA.JK", "ALMI.JK", "BAJA.JK", "BTON.JK", "CTBN.JK", "DPNS.JK", "EKAD.JK", "ETWA.JK", "GDST.JK", "IAAS.JK", "IGAR.JK", "INAI.JK", "INCI.JK", "ISSP.JK", "KBRI.JK", "KDSI.JK", "KIAS.JK", "NIKL.JK", 
"JIHD.JK", "SMDR.JK", "SMMT.JK", "SPMA.JK", "TOTO.JK", "BSDE.JK", "PWON.JK", "SMRA.JK", "CTRA.JK", "ASRI.JK", "MKPI.JK", "DILD.JK", "LPCK.JK", "LPKR.JK", "DMAS.JK", "BEST.JK", "KIJA.JK", "MTLA.JK", "JRPT.JK", "ADCP.JK", "AMAN.JK", "APLN.JK", "ARMY.JK", "BAPA.JK", "BAPI.JK", "BBSS.JK", "BCIP.JK", "BIKA.JK", "BIPP.JK", "BKDP.JK", 
"BKSL.JK", "COCO.JK", "CPRI.JK", "CSIS.JK", "DUTI.JK", "ELTY.JK", "EMDE.JK", "FMII.JK", "FORZ.JK", "GAMA.JK", "GMTD.JK", "GPRA.JK", "GWSA.JK", "HDIT.JK", "INPP.JK", "BIRD.JK", "ASSA.JK", "SMDR.JK", "TMAS.JK", "GIAA.JK", "NELY.JK", "BLUE.JK", "PSSI.JK", "ELPI.JK", "HUMI.JK", "JAYA.JK", "PORT.JK", "SDMU.JK", "AKSI.JK", "BESS.JK", 
"BPTR.JK", "COAL.JK", "GTSI.JK", "HELI.JK", "HOPE.JK", "IPCC.JK", "KAYU.JK", "MIRA.JK", "PBSA.JK", "SAFE.JK", "SAPX.JK", "SHIP.JK", "TNCA.JK", "TRUK.JK", "AYLS.JK", "BNBR.JK", "MERI.JK", "POLA.JK", "SURI.JK", "FUJI.JK",
"NZIA.JK", "GSMF.JK", "RGAS.JK", "YPAS.JK", "TOOL.JK", "OILS.JK", "BAIK.JK", "ASPR.JK", "CGAS.JK", "EURO.JK", "AIMS.JK", "ASPI.JK", "BELL.JK", "ZYRX.JK", "BRMS.JK", "POLI.JK", "ARCI.JK", "HRTA.JK", "EMAS.JK", "RLCO.JK", "CUAN.JK", "CDIA.JK", "PTRO.JK", "BUVA.JK", "MINA.JK", "PADI.JK", "BRNA.JK", "AKPI.JK", "ESIP.JK", "IPOL.JK",
"PACK.JK", "PBID.JK", "JARR.JK", "PGUN.JK", "UANG.JK", "FAST.JK", "PPRE.JK", "ALII.JK", "ERAL.JK", "DATA.JK", "DOOH.JK", "KIOS.JK", "PBRX.JK", "TRIS.JK", "NETV.JK", "INOV.JK", "PSAB.JK", "COIN.JK", "MDIA.JK", "BULL.JK", "SINI.JK", "UNIQ.JK", "ACRO.JK", "MYRA.JK", "WIFI.JK", "AWAN.JK", "CBDK.JK", "ESTI.JK", "ERTX.JK", "OKAS.JK",
"IFII.JK", "SOCI.JK", "PDPP.JK", "RATU.JK", "JGLE.JK", "PSKT.JK", "BBHI.JK", "KUAS.JK", "RMKO.JK", "CLAY.JK", "ENAK.JK", "VKTR.JK", "PART.JK", "UNSP.JK", "ZATA.JK", "BSKL.JK", "AMMN.JK", "TKIM.JK", "KRAS.JK", "NICL.JK", "DKFT.JK", "FORE.JK", "FPNI.JK", "SOLA.JK", "SMBR.JK", "SMGA.JK", "WTON.JK", "DAAZ.JK", "CHEM.JK", "BSBK.JK", 
"DKHH.JK", "OPMS.JK", "SSMS.JK", "MINE.JK", "NICE.JK", "PPRI.JK", "NPGF.JK", "SRSN.JK", "CITA.JK", "MOLI.JK", "UDNG.JK", "SMLE.JK", "DGWG.JK", "KAQI.JK", "CLPI.JK", "UNTD.JK",
"MDKI.JK", "BLES.JK", "IFSH.JK", "BATR.JK", "FWCT.JK", "GGRP.JK", "TBMS.JK", "INCF.JK", "SAMF.JK", "SWID.JK", "LTLS.JK", "OBMD.JK", "UNIC.JK", "SMKL.JK", "CMNT.JK", "KKES.JK", "YELO.JK", "AADI.JK", "CBRE.JK", "LEAD.JK", "BSSR.JK", "ATLA.JK", "FIRE.JK", "DSSA.JK", "BBRM.JK", "PSAT.JK", "MAHA.JK", "TPMA.JK", "BOAT.JK", "WINS.JK", "SICO.JK", "MBAP.JK", "BSML.JK", "MEJA.JK", "ITMA.JK", "DWGL.JK", "GTBO.JK", "ARII.JK", "MKAP.JK", "RIGS.JK", "CANI.JK", "PTIS.JK", "SUNI.JK", "GZCO.JK", "BWPT.JK",
"ASHA.JK", "CPRO.JK", "WMUU.JK", "NASI.JK", "SIMP.JK", "CLEO.JK", "HOKI.JK", "SMAR.JK", "AYAM.JK", "DSFI.JK", "PTPS.JK", "NSSS.JK", "DEWI.JK", "ISEA.JK", "CMRY.JK", "ANJT.JK", "WAPO.JK", "JAWA.JK", "CSRA.JK", "DPUM.JK", "NEST.JK", "GULA.JK", "PSDN.JK", "IBOS.JK", "STRK.JK", "TAYS.JK", "KEJU.JK", "PSGO.JK", "BISI.JK", "ENZO.JK", "GRPM.JK", "NAYZ.JK", "YUPI.JK", "TLDN.JK", "MKTR.JK", "CRAB.JK", "FISH.JK", "BOBA.JK", "SUPA.JK", "BBYB.JK", "BBKP.JK", "INPC.JK", "TRUE.JK", "MHKI.JK", "LAJU.JK",] 

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Scanner Settings")
    scanner_mode = st.radio("Pilih Mode Scanner:", ["Standard Accum", "Bottom Radar (Z-Score)"])
    st.divider()
    min_turnover = st.number_input("Min Transaksi (Miliar Rp)", value=1.0, step=0.5) * 1_000_000_000
    rvol_threshold = st.slider("Min Relative Volume", 1.0, 5.0, 1.2)
    atr_period_val = st.number_input("ATR Period (for TP/SL)", value=14)
    st.info("Scanner refresh otomatis tiap 180 detik.")

# --- CORE LOGIC FUNCTIONS ---
def apply_quant_logic(df, atr_p=14):
    df['CLV'] = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low'])
    df['CLV'] = df['CLV'].fillna(0)
    mfv = df['CLV'] * df['Volume']
    df['CMF'] = mfv.rolling(20).sum() / df['Volume'].rolling(20).sum()
    
    df['Mean_20'] = df['Close'].rolling(20).mean()
    df['Std_20'] = df['Close'].rolling(20).std()
    df['Z_Score'] = (df['Close'] - df['Mean_20']) / df['Std_20']
    
    df['NetVol'] = np.where(df['Close'] > df['Close'].shift(1), df['Volume'], -df['Volume'])
    df['NetVol_5D'] = df['NetVol'].rolling(5).sum()
    df["AvgVolume"] = df["Volume"].rolling(20).mean()
    df["RelVolume"] = df["Volume"] / df["AvgVolume"]
    df["High20"] = df["High"].rolling(20).max()
    df["Low20"] = df["Low"].rolling(20).min()
    df["ROC"] = df["Close"].pct_change(5)
    
    tr = pd.concat([df['High']-df['Low'], abs(df['High']-df['Close'].shift()), abs(df['Low']-df['Close'].shift())], axis=1).max(axis=1)
    df['ATR'] = tr.rolling(atr_p).mean()
    return df

@st.cache_data(ttl=60)
def fetch_data(stock_list):
    return yf.download(stock_list, period="1y", group_by='ticker', progress=False)

# --- MAIN EXECUTION ---
try:
    all_data = fetch_data(stocks)
    results = []

    for stock in stocks:
        try:
            df = all_data[stock].copy().dropna()
            if len(df) < 30: continue
            
            df = apply_quant_logic(df, atr_period_val)
            latest = df.iloc[-1]
            turnover = latest["Close"] * latest["Volume"]
            
            if turnover < min_turnover: continue
            
            # Logic Distribution Check
            is_selling = "NORMAL"
            if latest["Close"] <= df["Low20"].iloc[-2] or (latest["Close"] < latest["Open"] and latest["NetVol_5D"] < 0):
                is_selling = "DISTRIBUTION 📉"

            # Scoring Logic
            score = 0
            entry = "WAIT"
            if scanner_mode == "Standard Accum":
                if latest["RelVolume"] > rvol_threshold: score += 1
                if latest["Close"] > latest["Open"] and latest["CLV"] > 0.4: score += 1
                if latest["Close"] >= latest["High20"]: score += 1
                if latest["CMF"] > 0.05: score += 1
                if score >= 3: entry = "BUY 🔥"
                elif score == 2: entry = "WATCH 👀"
            else:
                if latest["Z_Score"] < -2.0: score += 2
                if latest["CMF"] > 0: score += 1
                if latest["RelVolume"] > 1.0: score += 1
                if score >= 3: entry = "BOTTOMING 🛡️"

            tp_level = latest["Close"] + (2 * latest["ATR"])
            sl_level = latest["Close"] - (1.5 * latest["ATR"])
            impact = "HIGH ✅" if turnover > 50e9 else "MEDIUM ⚠️" if turnover > 10e9 else "LOW 🔴"

            results.append({
                "Ticker": stock, "Price": int(latest["Close"]),
                "Z-Score": round(latest["Z_Score"], 4),
                "Net Flow": "Accum" if latest["CMF"] > 0 else "Sell",
                "ROC 5D (%)": round(latest["ROC"] * 100, 2),
                "R-Vol": round(latest["RelVolume"], 2),
                "Turnover (M)": round(turnover / 1_000_000, 2),
                "Impact": impact, "Status": is_selling,
                "TP (ATR)": int(tp_level), "SL (ATR)": int(sl_level),
                "Score": score, "Signal": entry
            })
        except: continue

    df_final = pd.DataFrame(results)

    if not df_final.empty:
        df_final = df_final.sort_values(by="Score", ascending=False)
        
        # --- SUMMARY HEADER ---
        c1, c2, c3 = st.columns(3)
        c1.metric("Mode Active", scanner_mode)
        c2.metric("Saham Lolos Filter", len(df_final))
        buy_signals = df_final[df_final["Signal"].str.contains("BUY|BOTTOMING")]
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
                now_jkt = datetime.now(jakarta_tz).strftime('%H:%M')
                msg = f"🛰️ *[{scanner_mode}] Alert ({now_jkt} WIB)*\n"
                msg += "----------------------------\n"
                for t in new_to_notify:
                    row = buy_signals[buy_signals['Ticker'] == t].iloc[0]
                    msg += f"• *{row['Ticker']}* | Price: {row['Price']}\n"
                    msg += f"  📊 ROC: {row['ROC 5D (%)']}% | R-Vol: {row['R-Vol']}\n"
                    msg += f"  📈 Z-Score: {row['Z-Score']} | Flow: {row['Net Flow']}\n"
                    msg += f"  🎯 TP: {row['TP (ATR)']} | 🛑 SL: {row['SL (ATR)']}\n"
                    msg += f"  🏷️ {row['Signal']}\n\n"
                
                send_telegram(msg)
                st.session_state.last_sent_tickers.update(new_to_notify)
            
            st.session_state.last_sent_tickers = st.session_state.last_sent_tickers.intersection(current_buy_tickers)

        # --- FULL MARKET RESULTS ---
        st.subheader("📊 Full Market Radar Results")
        st.dataframe(df_final, use_container_width=True)

        # --- BACKTEST ENGINE ---
        st.divider()
        with st.expander("📊 Logic Backtest Engine (6 Month Performance Check)"):
            st.write("Cek performa Signal dalam 5 hari ke depan.")
            if st.button("Run Backtest Now 🚀"):
                bt_results = []
                for s in stocks[:100]:
                    try:
                        d_bt = all_data[s].dropna()
                        d_bt = apply_quant_logic(d_bt)
                        for i in range(40, len(d_bt)-5):
                            r = d_bt.iloc[i]
                            if r["RelVolume"] > 1.2 and r["CMF"] > 0.05 and r["Close"] >= r["High20"]:
                                p_entry = r["Close"]
                                p_exit = d_bt.iloc[i+5]["Close"]
                                bt_results.append(((p_exit - p_entry)/p_entry)*100)
                    except: continue
                
                if bt_results:
                    arr = np.array(bt_results)
                    win_rate = (len(arr[arr > 0]) / len(arr)) * 100
                    st.success(f"Backtest Result: Win Rate {round(win_rate, 2)}% | Avg Profit {round(np.mean(arr), 2)}%")
    else:
        st.warning("Belum ada saham yang masuk kriteria.")

except Exception as e:
    st.error(f"Error Global: {e}")

# --- REFRESH ---
st.caption(f"Last update: {datetime.now(jakarta_tz).strftime('%H:%M:%S')} WIB")
time.sleep(180)
st.rerun()
