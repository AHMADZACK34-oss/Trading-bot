import os
import requests
import yfinance as yf
from datetime import datetime
import time

def hantar_ke_telegram():
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    CHAT_ID = '5217743374'
    
    # Pastikan file senarai.txt wujud dalam repo kau
    with open('senarai.txt', 'r') as f:
        senarai_saham = [line.strip() for line in f.readlines() if line.strip()]

    print(f"Jumlah saham nak diproses: {len(senarai_saham)}")

    for i in range(0, len(senarai_saham), 10):
        chunk = senarai_saham[i:i+10]
        laporan = f"<b>MASTER DATA - {datetime.now().strftime('%d/%m/%y')}</b>\n\n"
        
        for s in chunk:
            try:
                ticker = yf.Ticker(s)
                # Pakai fast_info supaya lebih laju dan tak mudah error
                info = ticker.fast_info
                harga = info['last_price']
                
                # Kita letak data ringkas dulu supaya bot laju
                laporan += f"<b>{s}</b> | ${harga:.2f}\n"
            except Exception as e:
                laporan += f"<b>{s}</b> | Error: {str(e)[:5]}\n"
                continue # PENTING: Ini yang buat dia tak stop kalau error
        
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={'chat_id': CHAT_ID, 'text': laporan, 'parse_mode': 'HTML'})
        
        time.sleep(3) # Delay 3 saat supaya Telegram tak block

if __name__ == "__main__":
    hantar_ke_telegram()
