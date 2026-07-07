import os
import requests
import yfinance as yf

# 1. Masukkan harga beli anda di sini
# Contoh: 'NVDA': 185.00 bermaksud anda beli NVDA pada harga $185.00
PORTFOLIO = {
    'NVDA': 185.00, 'AAPL': 295.00, 'TSLA': 400.00, 'AMD': 520.00, 'DELL': 400.00,
    'AVGO': 350.00, 'ORCL': 140.00, 'PLTR': 125.00, 'INTC': 115.00, 'NVO': 45.00,
    'SPCX': 155.00, 'WMT': 105.00, 'BAC': 55.00, 'NOW': 100.00, '0166.KL': 2.10
}

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = '5217743374'

def hantar_telegram(mesej):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={'chat_id': CHAT_ID, 'text': mesej, 'parse_mode': 'HTML'})

laporan = "🚨 <b>ALERT: TARGET 5% TERCAPAI!</b>\n"
ada_untung = False

for s, harga_beli in PORTFOLIO.items():
    try:
        stock = yf.Ticker(s)
        hist = stock.history(period="1d")
        if not hist.empty:
            harga_semasa = hist['Close'].iloc[-1]
            profit_pct = ((harga_semasa - harga_beli) / harga_beli) * 100
            
            # Jika untung 5% ke atas, tambah dalam mesej
            if profit_pct >= 5.0:
                laporan += f"\n<b>{s}</b>: ${harga_semasa:.2f}\nUntung: {profit_pct:.2f}% 🚀 <b>JUAL SEKARANG!</b>\n"
                ada_untung = True
    except:
        continue

# Hanya hantar mesej jika ada kaunter yang capai target 5%
if ada_untung:
    hantar_telegram(laporan)
