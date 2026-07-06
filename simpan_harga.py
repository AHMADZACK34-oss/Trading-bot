import yfinance as yf
from ta.trend import SMAIndicator, EMAIndicator
from ta.momentum import RSIIndicator
import requests

TOKEN = "8158820985:AAFq3SJngnxZ__fPWcyGEzBVHdBhm4TxN2g"
CHAT_ID = "5217743374"

def hantar_telegram(mesej):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mesej}"
    try:
        requests.get(url)
    except:
        pass

watchlist = ["NVDA", "AAPL", "TSM", "MSFT", "GOOGL"]

for simbol in watchlist:
    saham = yf.Ticker(simbol)
    data = saham.history(period="6mo")
    if not data.empty:
        ma50 = SMAIndicator(close=data['Close'], window=50).sma_indicator().iloc[-1]
        ema20 = EMAIndicator(close=data['Close'], window=20).ema_indicator().iloc[-1]
        rsi = RSIIndicator(close=data['Close'], window=14).rsi().iloc[-1]
        harga = data['Close'].iloc[-1]
        
        if harga > ema20 and rsi < 60:
            hantar_telegram(f"SIGNAL BELI: {simbol} pada {harga:.2f}")
            print(f"Signal dihantar: BELI {simbol}")
        elif harga < ma50:
            hantar_telegram(f"JUAL/CUT LOSS: {simbol} pada {harga:.2f}")
            print(f"Signal dihantar: JUAL {simbol}")
