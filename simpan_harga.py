import os
import requests

# Mengambil token dari GitHub Secrets
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = '5217743374'
mesej = "Ujian Bot Berjaya!"

# URL penuh untuk menghantar mesej
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mesej}"

# Menghantar permintaan terus ke Telegram
response = requests.get(url)

# Mencetak hasil untuk kita lihat dalam log
print(f"Status Kod: {response.status_code}")
print(f"Respon Telegram: {response.text}")
