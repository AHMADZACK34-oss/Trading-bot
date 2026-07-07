import os
import requests
import yfinance as yf

# Mengambil token dari GitHub Secrets
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = '5217743374'

portfolio = {"NVDA": 120.00, "AAPL": 150.00}

def hantar_telegram(mesej):
    if TOKEN:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        params = {'chat_id': CHAT_ID, 'text': mesej}
        try:
            requests.get(url, params=params)
        except Exception as e:
            print(f"Gagal hantar mesej: {e}")

for simbol, harga_beli in portfolio.items():
    saham = yf.Ticker(simbol)
    data = saham.history(period="1d")
    
    if not data.empty:
        harga_semasa = data['Close'].iloc[-1]
        peratus_untung = ((harga_semasa - harga_beli) / harga_beli) * 100
        
        mesej = f"Saham {simbol}: Harga semasa ${harga_semasa:.2f}, Untung/Rugi: {peratus_untung:.2f}%"
        hantar_telegram(mesej)
