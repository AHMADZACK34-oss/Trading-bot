import yfinance as yf
import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = '5217743374'

def hantar(pesan):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': pesan, 'parse_mode': 'HTML'})

def analisa_saham(ticker_list):
    laporan = "📈 <b>LAPORAN ANALISIS PRO</b>\n"
    for s in ticker_list:
        t = yf.Ticker(s)
        hist = t.history(period="1mo")
        info = t.info
        
        # Data Asas
        close = hist['Close'].iloc[-1]
        volume = hist['Volume'].iloc[-1]
        avg_vol = hist['Volume'].mean()
        
        # Teknikal (RSI Ringkas)
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs.iloc[-1]))
        
        # Fundamental & Jerung
        pe = info.get('forwardPE', 0)
        pm = info.get('profitMargins', 0) * 100
        jerung = "🦈 AKTIF" if volume > avg_vol * 1.5 else "⚪ BIASA"
        
        # Logik Keputusan
        keputusan = "HOLD"
        if rsi < 30 and pe < 20: keputusan = "🛒 BUY (Murah & Potensi)"
        elif rsi > 70: keputusan = "💰 SELL (Overbought)"
        elif volume > avg_vol * 2: keputusan = "🚀 BUY (Lonjakan Jerung)"
        
        laporan += f"\n<b>{s}</b>: ${close:.2f}\n"
        laporan += f"• Keputusan: {keputusan}\n"
        laporan += f"• Jerung: {jerung} | RSI: {rsi:.1f}\n"
        laporan += f"• PE: {pe:.1f} | Margin: {pm:.1f}%\n"
    
    hantar(laporan)

analisa_saham(['NVDA', 'AAPL', 'TSLA', 'ORCL', 'WMT'])
