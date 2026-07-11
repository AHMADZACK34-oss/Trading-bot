import os
import requests
import yfinance as yf
from datetime import datetime

def hantar_ke_telegram():
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    CHAT_ID = '5217743374'
    
    # Letak 500 saham kau kat sini (pastikan list ni lengkap)
    senarai_saham = ['AMD', 'ARM', 'ISRG', 'NVDA', 'AAPL', 'MSFT', 'TSLA'] # Tambah lagi sampai 500
    
    # Fungsi untuk pecahkan mesej supaya Telegram tak block
    def chunk_list(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    # Kita hantar 10 saham setiap satu mesej (supaya tak kena block)
    for chunk in chunk_list(senarai_saham, 10):
        laporan = "<b>MASTER DATA - TUAN ZAHRAN</b>\n\n"
        for s in chunk:
            try:
                ticker = yf.Ticker(s)
                info = ticker.info
                harga = info.get('currentPrice', 'N/A')
                pe = info.get('trailingPE', 'N/A')
                cap = info.get('marketCap', 0) / 1e9
                div = info.get('dividendYield', 0) * 100
                
                laporan += f"<b>{s} | HOLD | ${harga}</b>\n• PE: {pe} | Cap: ${cap:.1f}B | Div: {div:.1f}%\n--------------------\n"
            except:
                laporan += f"<b>{s}:</b> Error\n"
        
        # Hantar mesej demi mesej
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {'chat_id': CHAT_ID, 'text': laporan, 'parse_mode': 'HTML'}
        requests.post(url, data=payload)

if name == "__main__":
    hantar_ke_telegram()
