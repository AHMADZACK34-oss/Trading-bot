import os
import requests
import yfinance as yf
from datetime import datetime

def hantar_ke_telegram():
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    CHAT_ID = '5217743374'
    
    # Senarai saham yang kau nak pantau
    senarai_saham = ['AMD', 'WDC', 'INTC', 'TSLA', 'AAPL', 'NVDA', 'MSFT', 'META', 'GOOGL']
    
    waktu_skrg = datetime.now().strftime('%d/%m/%y %I:%M %p')
    laporan = f"<b>LIVE DATA - TUAN ZAHRAN</b>\n<i>Data: {waktu_skrg}</i>\n\n"
    
    for s in senarai_saham:
        try:
            # force_download=True memastikan data bukan dari cache lama
            ticker = yf.Ticker(s)
            data = ticker.history(period='1d', interval='1m')
            if not data.empty:
                harga_terkini = data['Close'].iloc[-1]
                laporan += f"<b>{s}:</b> ${harga_terkini:.2f}\n"
            else:
                laporan += f"<b>{s}:</b> Tiada data\n"
        except:
            laporan += f"<b>{s}:</b> Error\n"
            
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': laporan, 'parse_mode': 'HTML'}
    requests.post(url, data=payload)

if __name__ == "__main__":
    hantar_ke_telegram()
