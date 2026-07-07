import yfinance as yf, requests, os
from gtts import gTTS

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = '5217743374'

def hantar(teks, suara=None):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': teks, 'parse_mode': 'HTML'})
    if suara and os.path.exists(suara):
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendVoice", data={'chat_id': CHAT_ID}, files={'voice': open(suara, 'rb')})

senarai_saham = ['AMD', 'WDC', 'INTC', 'TSLA', 'AAPL', 'NVDA', 'MSFT', 'NVO', 'BAC', 'ORCL', 'IVV', 'MCD', 'GOOGL', 'PLTR', 'SAP', 'META', 'AMZN', 'JEPQ', 'WMT', 'DELL', 'ARM', 'ISRG']
laporan = "🧠 <b>MASTER TERMINAL PRO - TUAN ZAHRAN</b>\n"

for s in senarai_saham:
    t = yf.Ticker(s)
    info = t.info
    hist = t.history(period="1mo")
    
    if not hist.empty:
        curr = hist['Close'].iloc[-1]
        ytd = info.get('ytdReturn', 0) * 100
        m_cap = info.get('marketCap', 0) / 1e9
        div = info.get('dividendYield', 0) * 100
        pe = info.get('trailingPE', 0)
        # Margin ditambah semula di sini
        margin = (info.get('profitMargins', 0) or 0) * 100
        
        # Berita Terkini
        news = t.news
        news_text = "Tiada berita."
        if news and isinstance(news, list):
            titles = [n.get('title', 'Tiada tajuk') for n in news[:2]]
            news_text = "\n".join([f"• {t}" for t in titles])
        
        status = "HOLD"
        if ytd > 10: status = "🛒 BUY (Uptrend)"
        elif ytd < -10: status = "⚠️ SELL (Downtrend)"
        
        laporan += (f"\n<b>{s}</b> | {status} | ${curr:.2f}\n"
                    f"• YTD: {ytd:.1f}% | PE: {pe:.1f} | Margin: {margin:.1f}%\n"
                    f"• Cap: ${m_cap:.1f}B | Div: {div:.1f}%\n"
                    f"• Berita:\n{news_text}\n"
                    f"----------------------------")

        if "BUY" in status:
            tts = gTTS(text=f"BUY. Tahniah Tuan Zahran, {s} dalam trend positif.", lang='ms')
            tts.save("jarvis.mp3")
            hantar(f"🚀 <b>TAHNIAH!</b> Signal BUY untuk {s}.", "jarvis.mp3")
        elif "SELL" in status:
            tts = gTTS(text=f"SELL. Amaran Tuan Zahran, {s} dalam trend negatif.", lang='ms')
            tts.save("jarvis.mp3")
            hantar(f"⚠️ <b>BAHAYA!</b> Signal SELL untuk {s}.", "jarvis.mp3")

hantar(laporan)
