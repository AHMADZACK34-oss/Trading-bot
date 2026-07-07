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

def analisa_pasaran():
    senarai_saham = ['NVDA', 'AAPL', 'TSLA']
    laporan = "🧠 <b>LAPORAN JARVIS AI</b>\n"
    
    for s in senarai_saham:
        t = yf.Ticker(s)
        hist = t.history(period="1mo")
        
        if hist.empty:
            continue
            
        current = hist['Close'].iloc[-1]
        volume = hist['Volume'].iloc[-1]
        avg_vol = hist['Volume'].mean()
        
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rsi = 100 - (100 / (1 + (gain.iloc[-1] / loss.iloc[-1])))
        
        status_jerung = "🦈 AKTIF" if volume > avg_vol * 1.5 else "⚪ BIASA"
        peratus_perubahan = ((current - hist['Open'].iloc[0]) / hist['Open'].iloc[0]) * 100
        
        laporan += f"\n<b>{s}</b>: ${current:.2f} ({peratus_perubahan:+.1f}%)\n"
        laporan += f"• RSI: {rsi:.1f} | Jerung: {status_jerung}\n"
        
        if peratus_perubahan >= 5.0:
            teks_suara = f"Tahniah Tuan Ahmad! Saham {s} telah melonjak {peratus_perubahan:.0f} peratus."
            tts = gTTS(text=teks_suara, lang='ms')
            tts.save("jarvis.mp3")
            hantar_ke_telegram(f"🚀 <b>TAHNIAH!</b> {s} naik {peratus_perubahan:.1f}%", "jarvis.mp3")
            
        elif peratus_perubahan <= -3.0:
            teks_suara = f"Amaran Tuan Ahmad! Saham {s} jatuh sebanyak {abs(peratus_perubahan):.0f} peratus."
            tts = gTTS(text=teks_suara, lang='ms')
            tts.save("jarvis.mp3")
            hantar_ke_telegram(f"⚠️ <b>BAHAYA!</b> {s} jatuh {peratus_perubahan:.1f}%", "jarvis.mp3")
            
    hantar_ke_telegram(laporan)

if name == "__main__":
    analisa_pasaran()
