import yfinance as yf, requests, os
from gtts import gTTS

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = '5217743374'

def hantar(teks, suara=None):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': teks, 'parse_mode': 'HTML'})
    if suara and os.path.exists(suara):
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendVoice", data={'chat_id': CHAT_ID}, files={'voice': open(suara, 'rb')})

senarai_saham = ['AMD', 'WDC', 'INTC', 'TSLA', 'AAPL', 'NVDA', 'MSFT', 'NVO', 'BAC', 'ORCL', 'IVV', 'MCD', 'GOOGL', 'PLTR', 'SAP', 'META', 'AMZN', 'JEPQ', 'WMT', 'DELL', 'ARM', 'ISRG']
laporan = "🧠 <b>LAPORAN ANALISIS PRO - TUAN ZAHRAN</b>\n"

for s in senarai_saham:
    t = yf.Ticker(s)
    hist = t.history(period="1wk")
    info = t.info
    
    if not hist.empty:
        current = hist['Close'].iloc[-1]
        peratus = ((current - hist['Open'].iloc[0]) / hist['Open'].iloc[0]) * 100
        
        # Logik Keputusan
        keputusan = "HOLD"
        if peratus >= 5.0: keputusan = "🛒 BUY (Murah & Potensi)"
        elif peratus <= -3.0: keputusan = "⚠️ SELL (Bahaya)"
        
        # Data Tambahan
        pe = info.get('trailingPE', 0)
        margin = info.get('profitMargins', 0) * 100
        rsi = "N/A" # Perlu library teknikal jika nak nilai tepat
        
        laporan += f"\n<b>{s}</b>: ${current:.2f}\n• Keputusan: {keputusan}\n• PE: {pe:.1f} | Margin: {margin:.1f}%\n"

        # Suara Terus (Tanpa Eja)
        if peratus >= 5.0:
            tts = gTTS(text=f"BUY. Tahniah Tuan Zahran, {s} naik {peratus:.0f} peratus.", lang='ms')
            tts.save("jarvis.mp3")
            hantar(f"🚀 <b>TAHNIAH!</b> {s} naik {peratus:.1f}%.", "jarvis.mp3")
        elif peratus <= -3.0:
            tts = gTTS(text=f"SELL. Amaran Tuan Zahran, {s} jatuh {abs(peratus):.0f} peratus.", lang='ms')
            tts.save("jarvis.mp3")
            hantar(f"⚠️ <b>BAHAYA!</b> {s} jatuh {abs(peratus):.1f}%.", "jarvis.mp3")

hantar(laporan)
