import os, requests, yfinance as yf, json, datetime

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = '5217743374'
SYMBOLS = ['NVDA', 'AAPL', 'TSLA', 'AMD', 'DELL', 'AVGO', 'ORCL', 'PLTR', 'INTC', 'NVO', 'SPCX', 'WMT', 'BAC', 'NOW', '0166.KL']
FILE = 'harga_harian.json'

def hantar(text):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'HTML'})

hari_ini = datetime.date.today().isoformat()
if os.path.exists(FILE):
    with open(FILE, 'r') as f: data = json.load(f)
else:
    data = {'tarikh': '', 'rujukan': {}}

if data['tarikh'] != hari_ini:
    data['rujukan'] = {s: yf.Ticker(s).history(period="1d")['Close'].iloc[-1] for s in SYMBOLS}
    data['tarikh'] = hari_ini
    with open(FILE, 'w') as f: json.dump(data, f)
    hantar(f"✅ <b>Rujukan harga untuk {hari_ini} telah ditetapkan!</b>")

pesan = f"📊 <b>LAPORAN JERUNG {hari_ini}</b>\n"
perlu_hantar = False

for s in SYMBOLS:
    try:
        t = yf.Ticker(s)
        df = t.history(period="15d")
        harga = df['Close'].iloc[-1]
        volume = df['Volume'].iloc[-1]
        avg_vol = df['Volume'].iloc[-11:-1].mean()
        
        untung = ((harga - data['rujukan'][s]) / data['rujukan'][s]) * 100
        
        # Logik Amaran
        if untung >= 5.0:
            # Jika volume tinggi, kita letak Tanda Jerung 🦈
            vol_icon = "🦈" if volume > avg_vol else "🚀"
            pesan += f"\n{vol_icon} <b>{s}</b>: ${harga:.2f} (+{untung:.2f}%) - <b>TP!</b>"
            perlu_hantar = True
        elif untung <= -3.0:
            pesan += f"\n⚠️ <b>{s}</b>: ${harga:.2f} ({untung:.2f}%) - <b>SL!</b>"
            perlu_hantar = True
    except: continue

if perlu_hantar: hantar(pesan)
