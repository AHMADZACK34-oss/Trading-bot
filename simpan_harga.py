import os, requests, yfinance as yf, json, datetime

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = '5217743374'
SYMBOLS = ['NVDA', 'AAPL', 'TSLA', 'AMD', 'DELL', 'AVGO', 'ORCL', 'PLTR', 'INTC', 'NVO', 'SPCX', 'WMT', 'BAC', 'NOW', '0166.KL']
FILE = 'harga_harian.json'

def hantar(text):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'HTML'})

# Dapatkan tarikh hari ini
hari_ini = datetime.date.today().isoformat()

# Muat fail data
if os.path.exists(FILE):
    with open(FILE, 'r') as f: data = json.load(f)
else:
    data = {'tarikh': '', 'rujukan': {}}

# Jika hari sudah berubah, set semula rujukan
if data['tarikh'] != hari_ini:
    data['rujukan'] = {s: yf.Ticker(s).history(period="1d")['Close'].iloc[-1] for s in SYMBOLS}
    data['tarikh'] = hari_ini
    with open(FILE, 'w') as f: json.dump(data, f)
    hantar(f"✅ <b>Rujukan harga baru telah ditetapkan untuk {hari_ini}!</b>")

# Kira keuntungan berdasarkan rujukan hari ini
pesan = f"🚨 <b>ALERT: TARGET 5% DARI HARGA {hari_ini}!</b>\n"
ada = False
for s in SYMBOLS:
    try:
        harga = yf.Ticker(s).history(period="1d")['Close'].iloc[-1]
        untung = ((harga - data['rujukan'][s]) / data['rujukan'][s]) * 100
        if untung >= 5.0:
            pesan += f"\n<b>{s}</b>: ${harga:.2f} ({untung:.2f}%) 🚀 <b>JUAL!</b>"
            ada = True
    except: continue

if ada: hantar(pesan)
