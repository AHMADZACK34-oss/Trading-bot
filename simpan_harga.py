import os, requests, yfinance as yf, json

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = '5217743374'
SYMBOLS = ['NVDA', 'AAPL', 'TSLA', 'AMD', 'DELL', 'AVGO', 'ORCL', 'PLTR', 'INTC', 'NVO', 'SPCX', 'WMT', 'BAC', 'NOW', '0166.KL']
FILE = 'harga_malam.json'

def hantar(text):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'HTML'})

# 1. Kalau fail belum ada, bot akan tangkap harga hari ini sebagai rujukan
if not os.path.exists(FILE):
    rujukan = {s: yf.Ticker(s).history(period="1d")['Close'].iloc[-1] for s in SYMBOLS}
    with open(FILE, 'w') as f: json.dump(rujukan, f)
    hantar("✅ <b>Bot telah menetapkan harga rujukan untuk dipantau!</b>")
else:
    # 2. Kalau fail dah ada, bot akan kira untung
    with open(FILE, 'r') as f: rujukan = json.load(f)
    pesan = "🚨 <b>TARGET 5% TERCAPAI!</b>\n"
    ada = False
    for s in SYMBOLS:
        harga = yf.Ticker(s).history(period="1d")['Close'].iloc[-1]
        untung = ((harga - rujukan[s]) / rujukan[s]) * 100
        if untung >= 5.0:
            pesan += f"\n<b>{s}</b>: ${harga:.2f} ({untung:.2f}%) 🚀 <b>JUAL!</b>"
            ada = True
    if ada: hantar(pesan)
