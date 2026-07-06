import os
import yfinance as yf
import requests

# Mengambil token dari GitHub Secrets
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = "5217743374"

portfolio = {"NVDA": 120.00, "AAPL": 150.00}

def hantar_telegram(mesej):
    if TOKEN: # Pastikan token ada sebelum hantar
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mesej}"
        requests.get(url)

for simbol, harga_beli in portfolio.items():
    saham = yf.Ticker(simbol)
    data = saham.history(period="1d")
    if not data.empty:
        harga_semasa = data['Close'].iloc[-1]
        peratus_untung = ((harga_semasa - harga_beli) / harga_beli) * 100
        if peratus_untung >= 5.0:
            hantar_telegram(f"🔥 PROFIT ALERT! {simbol} sudah untung {peratus_untung:.2f}%. Sila pertimbangkan untuk JUAL!")
