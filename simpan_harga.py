import os
import requests
import yfinance as yf

# Tetapan Portfolio Anda
# Sila kemas kini BuyPrice, CutLoss, dan TakeProfit di sini apabila anda buat analisis baru
PORTFOLIO = {
    'NVDA': {'BuyPrice': 120.00, 'CutLoss': 100.00, 'TakeProfit': 160.00},
    'AAPL': {'BuyPrice': 180.00, 'CutLoss': 160.00, 'TakeProfit': 220.00}
}

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = '5217743374'

def hantar_telegram(mesej):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {'chat_id': CHAT_ID, 'text': mesej, 'parse_mode': 'HTML'}
    requests.get(url, params=params)

laporan = "📊 <b>LAPORAN PORTFOLIO HARIAN</b>\n"

for ticker, data in PORTFOLIO.items():
    # Ambil data harga semasa
    try:
        harga_semasa = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
        peratusan = ((harga_semasa - data['BuyPrice']) / data['BuyPrice']) * 100
        
        status = "HOLD ⚪"
        if harga_semasa <= data['CutLoss']:
            status = "⚠️ <b>CUT LOSS SEGERA!</b>"
        elif harga_semasa >= data['TakeProfit']:
            status = "💰 <b>TAKE PROFIT!</b>"
            
        laporan += f"\n<b>{ticker}</b>\nHarga: ${harga_semasa:.2f} ({peratusan:+.2f}%)\nStatus: {status}\n"
    except Exception as e:
        laporan += f"\n{ticker}: Gagal ambil data.\n"

hantar_telegram(laporan)
