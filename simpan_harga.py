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

senarai_saham = ['AMD', 'WDC', 'INTC', 'TSLA', 'AAPL', 'NVDA', 'MSFT', 'NVO', 'BAC', 'ORCL', 'IVV', 'MCD', 'GOOGL', 'PLTR', 'SAP', 'META', 'AMZN', 'JEPQ', 'WMT', 'DELL', 'ARM', 'ISRG']
laporan = "🧠 <b>LAPORAN ANALISIS JARVIS - TUAN ZAHRAN</b>\n"

for s in senarai_saham:
    t = yf.Ticker(s)
    hist = t.history(period="1wk")
    
    if not hist.empty:
        current = hist['Close'].iloc[-1]
        peratus_perubahan = ((current - hist['Open'].iloc[0]) / hist['Open'].iloc[0]) * 100
        
        # Logik Signal
        signal = "HOLD"
        if peratus_perubahan >= 5.0:
            signal = "BUY/TAKE PROFIT"
            laporan += f"\n• {s}: <b>{signal}</b> | ${current:.2f} (+{peratus_perubahan:.1f}%)"
            tts = gTTS(text=f"Signal bagi {s} adalah {signal}. Tahniah Tuan Zahran, saham ini telah naik {peratus_perubahan:.0f} peratus.", lang='ms')
            tts.save("jarvis.mp3")
            hantar_ke_telegram(f"🚀 <b>SIGNAL: {signal}</b>\n{s} naik {peratus_perubahan:.1f}%", "jarvis.mp3")
            
        elif peratus_perubahan <= -3.0:
            signal = "SELL/STOP LOSS"
            laporan += f"\n• {s}: <b>{signal}</b> | ${current:.2f} ({peratus_perubahan:.1f}%)"
            tts = gTTS(text=f"Signal bagi {s} adalah {signal}. Amaran Tuan Zahran, saham ini jatuh {abs(peratus_perubahan):.0f} peratus.", lang='ms')
            tts.save("jarvis.mp3")
            hantar_ke_telegram(f"⚠️ <b>SIGNAL: {signal}</b>\n{s} jatuh {abs(peratus_perubahan):.1f}%", "jarvis.mp3")
        
        else:
            laporan += f"\n• {s}: {signal} | ${current:.2f} ({peratus_perubahan:+.1f}%)"

hantar_ke_telegram(laporan)
