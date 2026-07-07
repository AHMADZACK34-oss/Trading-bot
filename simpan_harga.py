import yfinance as yf, requests, os
from gtts import gTTS
import pandas as pd

# Konfigurasi Telegram
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = '5217743374'

def hantar_ke_telegram(mesej, fail_suara=None):
    url_teks = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url_teks, data={'chat_id': CHAT_ID, 'text': mesej, 'parse_mode': 'HTML'})
    
    if fail_suara and os.path.exists(fail_suara):
        url_suara = f"https://api.telegram.org/bot{TOKEN}/sendVoice"
        files = {'voice': open(fail_suara, 'rb')}
        requests.post(url_suara, data={'chat_id': CHAT_ID}, files=files)

# Senarai saham penuh anda
senarai_saham = ['AMD', 'WDC', 'INTC', 'TSLA', 'AAPL', 'NVDA', 'MSFT', 'NVO', 'BAC', 'ORCL', 'IVV', 'MCD', 'GOOGL', 'PLTR', 'SAP', 'META', 'AMZN', 'JEPQ', 'WMT', 'DELL', 'ARM', 'ISRG']
laporan = "🧠 <b>LAPORAN JARVIS AI - SENARAI PENUH</b>\n"

for s in senarai_saham:
    t = yf.Ticker(s)
    hist = t.history(period="1mo")
    
    if not hist.empty:
        current = hist['Close'].iloc[-1]
        peratus_perubahan = ((current - hist['Open'].iloc[0]) / hist['Open'].iloc[0]) * 100
        laporan += f"\n• {s}: ${current:.2f} ({peratus_perubahan:+.1f}%)"
        
        # Amaran suara
        if peratus_perubahan >= 5.0:
            tts = gTTS(text=f"Tahniah Tuan Ahmad! Saham {s} naik {peratus_perubahan:.0f} peratus.", lang='ms')
            tts.save("jarvis.mp3")
            hantar_ke_telegram(f"🚀 <b>TAHNIAH!</b> {s} naik {peratus_perubahan:.1f}%", "jarvis.mp3")
        elif peratus_perubahan <= -3.0:
            tts = gTTS(text=f"Amaran Tuan Ahmad! Saham {s} jatuh {abs(peratus_perubahan):.0f} peratus.", lang='ms')
            tts.save("jarvis.mp3")
            hantar_ke_telegram(f"⚠️ <b>BAHAYA!</b> {s} jatuh {peratus_perubahan:.1f}%", "jarvis.mp3")

hantar_ke_telegram(laporan)
