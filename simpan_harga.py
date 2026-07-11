import os
import requests
import yfinance as yf
from datetime import datetime, timedelta

def hantar_ke_telegram():
    # Ambil token dari GitHub Secrets
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    CHAT_ID = '5217743374' # ID kau
    
    # Senarai saham
    senarai_saham = ['AMD', 'WDC', 'INTC', 'TSLA', 'AAPL', 'NVDA', 'MSFT', 'META', 'GOOGL']
    
    waktu_skrg = (datetime.utcnow() + timedelta(hours=8)).strftime('%d/%m/%y %I:%M %p')
    laporan = f"<b>MASTER TERMINAL PRO - TUAN ZAHRAN</b>\n<i>Data diambil: {waktu_skrg}</i>\n\n"
    
    for s in senarai_saham:
        try:
            ticker = yf.Ticker(s)
            harga = ticker.history(period='1d')['Close'].iloc[-1]
            laporan += f"<b>{s}:</b> ${harga:.2f}\n"
        except:
            laporan += f"<b>{s}:</b> Error\n"
            
    # Hantar ke Telegram
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': laporan, 'parse_mode': 'HTML'}
    requests.post(url, data=payload)

if name == "__main__":
    hantar_ke_telegram()
