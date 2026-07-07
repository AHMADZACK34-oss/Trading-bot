import yfinance as yf, requests, os
from gtts import gTTS
import pandas as pd

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = '5217743374'

def hantar(teks, suara=None):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': teks, 'parse_mode': 'HTML'})
    if suara and os.path.exists(suara):
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendVoice", data={'chat_id': CHAT_ID}, files={'voice': open(suara, 'rb')})

senarai_saham = ['AMD', 'WDC', 'INTC', 'TSLA', 'AAPL', 'NVDA', 'MSFT', 'NVO', 'BAC', 'ORCL', 'IVV', 'MCD', 'GOOGL', 'PLTR', 'SAP', 'META', 'AMZN', 'JEPQ', 'WMT', 'DELL', 'ARM', 'ISRG']
laporan = "🧠 <b>ANALISIS JARVIS - TUAN ZAHRAN</b>\n"

for s in senarai_saham:
    t = yf.Ticker(s)
    hist = t.history(period="1wk")
    if not hist.empty:
        current = hist['Close'].iloc[-1]
        peratus = ((current - hist['Open'].iloc[0]) / hist['Open'].iloc[0]) * 100
        
        # Tentukan status
        status = "BUY" if peratus >= 5.0 else ("SELL" if peratus <= -3.0 else "HOLD")
        laporan += f"\n• {s}: <b>{status}</b> ({peratus:+.1f}%)"
        
        # Jika kena syarat, hantar mesej amaran berasingan (Suara)
        if peratus >= 5.0:
            tts = gTTS(text=f"BUY. Tahniah Tuan Zahran, {s} naik {peratus:.0f} peratus.", lang='ms')
            tts.save("jarvis.mp3")
            hantar(f"🚀 <b>BUY!</b> {s} naik {peratus:.1f}%. Tahniah Tuan Zahran!", "jarvis.mp3")
        elif peratus <= -3.0:
            tts = gTTS(text=f"SELL. Amaran Tuan Zahran, {s} jatuh {abs(peratus):.0f} peratus.", lang='mp3')
            tts.save("jarvis.mp3")
            hantar(f"⚠️ <b>SELL!</b> {s} jatuh {abs(peratus):.1f}%. Amaran Tuan Zahran!", "jarvis.mp3")

hantar(laporan)
