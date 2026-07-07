import os
import requests
import yfinance as yf

# Senarai saham anda sahaja
SYMBOLS = ['NVDA', 'AAPL'] 
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = '5217743374'

def hantar_telegram(mesej):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={'chat_id': CHAT_ID, 'text': mesej, 'parse_mode': 'HTML'})

laporan = "📈 <b>LAPORAN TREND SEMASA</b>\n"

for s in SYMBOLS:
    stock = yf.Ticker(s)
    hist = stock.history(period="60d") # Ambil data 60 hari
    harga_semasa = hist['Close'].iloc[-1]
    ma50 = hist['Close'].rolling(window=50).mean().iloc[-1] # Kira purata 50 hari
    
    # Logik Jual/Beli Dinamik
    if harga_semasa > ma50:
        status = "BULLISH 🟢 (Trend Naik - Hold/Beli)"
    else:
        status = "BEARISH 🔴 (Trend Turun - Jual/Cut Loss)"
            
    laporan += f"\n<b>{s}</b>\nHarga: ${harga_semasa:.2f}\nMA50: ${ma50:.2f}\nStatus: {status}\n"

hantar_telegram(laporan)
