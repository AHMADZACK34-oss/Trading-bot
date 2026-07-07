import os
import requests
import yfinance as yf
import json

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = '5217743374'
SYMBOLS = ['NVDA', 'AAPL', 'TSLA', 'AMD', 'DELL', 'AVGO', 'ORCL', 'PLTR', 'INTC', 'NVO', 'SPCX', 'WMT', 'BAC', 'NOW', '0166.KL']

# Simpan harga rujukan dalam fail 'harga_malam.json'
FILENAME = 'harga_malam.json'

def hantar_telegram(mesej):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={'chat_id': CHAT_ID, 'text': mesej, 'parse_mode': 'HTML'})

# 1. Muat harga rujukan malam ini
if not os.path.exists(FILENAME):
    harga_rujukan = {}
    for s in SYMBOLS:
        stock = yf.Ticker(s)
        harga_rujukan[s] = stock.history(period="1d")['Close'].iloc[-1]
    with open(FILENAME, 'w') as f:
        json.dump(harga_rujukan, f)
    hantar_telegram("✅ <b>Bot telah menetapkan harga rujukan malam ini!</b>")

# 2. Kira keuntungan dari harga rujukan
with open(FILENAME, 'r') as f:
    harga_rujukan = json.load(f)

laporan = "🚨 <b>ALERT: TARGET 5% DARI HARGA MALAM INI!</b>\n"
ada_untung = False

for s in SYMBOLS:
    stock = yf.Ticker(s)
    harga_semasa = stock.history(period="1d")['Close'].iloc[-1]
    harga_beli = harga_rujukan[s]
    profit_pct = ((harga_semasa - harga_beli) / harga_beli) * 100
    
    if profit_pct >= 5.0:
        laporan += f"\n<b>{s}</b>: ${harga_semasa:.2f}\nUntung: {profit_pct:.2f}% 🚀 <b>JUAL SEKARANG!</b>\n"
        ada_untung = True

if ada_untung:
    hantar_telegram(laporan)
