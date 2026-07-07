import os, requests, yfinance as yf, json, datetime

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = '5217743374'
SYMBOLS = ['NVDA', 'AAPL', 'TSLA', 'AMD', 'DELL', 'AVGO', 'ORCL', 'PLTR', 'INTC', 'NVO', 'SPCX', 'WMT', 'BAC', 'NOW', '0166.KL']
FILE = 'harga_harian.json'

def hantar(text):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'HTML'})

def get_rsi(prices, n=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=n).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=n).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs.iloc[-1]))

hari_ini = datetime.date.today().isoformat()
if os.path.exists(FILE):
    with open(FILE, 'r') as f: data = json.load(f)
else:
    data = {'tarikh': '', 'rujukan': {}}

if data['tarikh'] != hari_ini:
    data['rujukan'] = {s: yf.Ticker(s).history(period="1d")['Close'].iloc[-1] for s in SYMBOLS}
    data['tarikh'] = hari_ini
    with open(FILE, 'w') as f: json.dump(data, f)
    hantar(f"✅ <b>Sistem Aktif - Rujukan: {hari_ini}</b>")

pesan = f"📊 <b>LAPORAN PRO {hari_ini}</b>\n"
perlu_hantar = False

for s in SYMBOLS:
    try:
        t = yf.Ticker(s)
        df = t.history(period="30d")
        harga = df['Close'].iloc[-1]
        
        # Pengiraan Teknikal Ringan
        ma20 = df['Close'].rolling(window=20).mean().iloc[-1]
        rsi = get_rsi(df['Close'])
        volume = df['Volume'].iloc[-1]
        avg_vol = df['Volume'].iloc[-11:-1].mean()
        
        untung = ((harga - data['rujukan'][s]) / data['rujukan'][s]) * 100
        
        if untung >= 5.0 and rsi < 75:
            vol_icon = "🦈" if volume > avg_vol else "🚀"
            pesan += f"\n{vol_icon} <b>{s}</b>: ${harga:.2f} (+{untung:.1f}%) | RSI: {rsi:.0f}"
            perlu_hantar = True
        elif untung <= -3.0:
            pesan += f"\n⚠️ <b>{s}</b>: ${harga:.2f} (SL! {untung:.1f}%)"
            perlu_hantar = True
    except: continue

if perlu_hantar: hantar(pesan)
