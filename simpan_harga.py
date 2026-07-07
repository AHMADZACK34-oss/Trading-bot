import yfinance as yf, requests, os
from gtts import gTTS

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = '5217743374'

def hantar(teks, suara=None):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': teks, 'parse_mode': 'HTML'})
    if suara and os.path.exists(suara):
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendVoice", data={'chat_id': CHAT_ID}, files={'voice': open(suara, 'rb')})

senarai_saham = ['AMD', 'WDC', 'INTC', 'TSLA', 'AAPL', 'NVDA', 'MSFT', 'NVO', 'BAC', 'ORCL', 'IVV', 'MCD', 'GOOGL', 'PLTR', 'SAP', 'META', 'AMZN', 'JEPQ', 'WMT', 'DELL', 'ARM', 'ISRG']
laporan = "🧠 <b>LAPORAN ANALISIS PRO (DOUBLE-CHECK) - TUAN ZAHRAN</b>\n"

for s in senarai_saham:
    t = yf.Ticker(s)
    hist_2wk = t.history(period="2wk")
    hist_1mo = t.history(period="1mo")
    info = t.info
    
    if not hist_2wk.empty and not hist_1mo.empty:
        curr = hist_2wk['Close'].iloc[-1]
        peratus_2wk = ((curr - hist_2wk['Open'].iloc[0]) / hist_2wk['Open'].iloc[0]) * 100
        peratus_1mo = ((curr - hist_1mo['Open'].iloc[0]) / hist_1mo['Open'].iloc[0]) * 100
        
        # Logik Double-Check: Signal hanya valid jika momentum 2 minggu & 1 bulan selari
        keputusan = "HOLD"
        if peratus_2wk >= 5.0 and peratus_1mo >= 0:
            keputusan = "🛒 BUY (Murah & Potensi)"
        elif peratus_2wk <= -3.0 or peratus_1mo <= -5.0:
            keputusan = "⚠️ SELL (Bahaya)"
        
        pe = info.get('trailingPE', 0)
        margin = info.get('profitMargins', 0) * 100
        laporan += f"\n<b>{s}</b>: ${curr:.2f}\n• Keputusan: {keputusan}\n• PE: {pe:.1f} | Margin: {margin:.1f}%\n"

        # Noti Suara (Terus Sebut BUY/SELL)
        if "BUY" in keputusan:
            tts = gTTS(text=f"BUY. Tahniah Tuan Zahran, {s} berada dalam trend positif.", lang='ms')
            tts.save("jarvis.mp3")
            hantar(f"🚀 <b>TAHNIAH!</b> {s} adalah signal BUY.", "jarvis.mp3")
        elif "SELL" in keputusan:
            tts = gTTS(text=f"SELL. Amaran Tuan Zahran, {s} menunjukkan kejatuhan.", lang='ms')
            tts.save("jarvis.mp3")
            hantar(f"⚠️ <b>BAHAYA!</b> {s} adalah signal SELL.", "jarvis.mp3")

hantar(laporan)
