import os, requests, yfinance as yf, json, datetime, pandas_ta as ta

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
    hantar(f"✅ <b>Rujukan baru untuk {hari_ini} telah ditetapkan!</b>")

pesan = f"📊 <b>ANALISIS PRO {hari_ini}</b>\n"
perlu_hantar = False

for s in SYMBOLS:
    try:
        t = yf.Ticker(s)
        df = t.history(period="6mo")
        info = t.info
        
        # Indikator Teknikal
        close = df['Close']
        ema200 = ta.ema(close, length=200).iloc[-1]
        ma50 = ta.sma(close, length=50).iloc[-1]
        rsi = ta.rsi(close, length=14).iloc[-1]
        macd = ta.macd(close).iloc[-1, 0] # MACD Line
        
        # Logik Jerung & Harga
        harga = close.iloc[-1]
        volume = df['Volume'].iloc[-1]
        avg_vol = df['Volume'].iloc[-11:-1].mean()
        untung = ((harga - data['rujukan'][s]) / data['rujukan'][s]) * 100
        
        # Fundamental (Profit Margin & PE)
        pm = info.get('profitMargins', 0) * 100
        pe = info.get('forwardPE', 0)
        
        # Signal Filtering (Pro Logic)
        if untung >= 5.0 and rsi < 75: # RSI < 75 elak Overbought
            vol_icon = "🦈" if volume > avg_vol else "🚀"
            pesan += f"\n{vol_icon} <b>{s}</b>: ${harga:.2f} (Untung: {untung:.1f}%)"
            pesan += f"\n   ↳ <i>RSI:{rsi:.0f} | MACD:{macd:.2f} | PM:{pm:.1f}% | PE:{pe:.1f}</i>"
            perlu_hantar = True
            
        elif untung <= -3.0:
            pesan += f"\n⚠️ <b>{s}</b>: ${harga:.2f} (SL! Rugi: {untung:.1f}%)"
            perlu_hantar = True
    except: continue

if perlu_hantar: hantar(pesan)
