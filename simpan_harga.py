import os
import requests
import yfinance as yf

# Ujian debug: kita guna print untuk lihat dalam log GitHub
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = '5217743374'

print(f"Token dikesan: {'YA' if TOKEN else 'TIDAK'}")

def hantar_telegram(mesej):
    if TOKEN:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        params = {'chat_id': CHAT_ID, 'text': mesej}
        response = requests.get(url, params=params)
        print(f"Status Kod Telegram: {response.status_code}")
        print(f"Respon Telegram: {response.text}")
    else:
        print("Token tiada!")

hantar_telegram("Ujian dari GitHub!")
