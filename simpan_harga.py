import os
import requests
import yfinance as yf
from datetime import datetime

def hantar_ke_telegram():
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    CHAT_ID = '5217743374'
    
    senarai_saham = ['AMD', 'ARM', 'ISRG'] # Tambah simbol lain di sini
    
    waktu_skrg = datetime.now().strftime('%d/%m/%y %I:%M %p')
    laporan = f"<b>MASTER DATA FUNDAMENTAL - TUAN ZAHRAN</b>\n<i>Data: {waktu_skrg}</i>\n\n"
    
    for s in senarai_saham:
        try:
            ticker = yf.Ticker(s)
            info = ticker.info
            
            # Tarik data lengkap
            harga = info.get('currentPrice', 'N/A')
            pe = info.get('trailingPE', 'N/A')
            cap = info.get('marketCap', 0) / 1e9 # Dalam Billion
            div = info.get('dividendYield', 0) * 100
            debt = info.get('totalDebt', 0) / 1e9 # Dalam Billion
            margin = info.get('profitMargins', 0) * 100
            
            laporan += (f"<b>{s} | HOLD | ${harga}</b>\n"
                        f"• PE: {pe} | Margin: {margin:.1f}%\n"
                        f"• Cap: ${cap:.1f}B | Debt: ${debt:.1f}B\n"
                        f"• Div: {div:.1f}% | Berita: Tiada tajuk\n"
                        f"------------------------------\n")
        except:
            laporan += f"<b>{s}:</b> Ralat data\n"
            
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': laporan, 'parse_mode': 'HTML'}
    requests.post(url, data=payload)

if __name__ == "__main__":
    hantar_ke_telegram()
