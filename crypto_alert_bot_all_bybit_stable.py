
import requests
import time
import telebot

API_KEY = 'udRZsZ1NQ0ELK0PSrS'
API_SECRET = 'bAjlUEKQBTBvdsHgs5lvy6VRX94b4xaT1Xoj'
TELEGRAM_BOT_TOKEN = '8047247430:AAHz-YvXSnhkxgdPOzbeXP81PZFz4llgvTM'
TELEGRAM_CHAT_ID = 7465646426

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def get_spot_symbols():
    url = "https://api.bybit.com/v5/market/instruments?category=spot"
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        if response.status_code != 200:
            return []
        data = response.json()
        return [item["symbol"] for item in data.get("result", {}).get("list", []) if item["symbol"].endswith("USDT")]
    except Exception as e:
        return []

def get_rsi(symbol, interval='1h', limit=200):
    url = f"https://api.bybit.com/v5/market/kline?category=spot&symbol={symbol}&interval={interval}&limit={limit}"
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        if response.status_code != 200:
            return None
        data = response.json()
        closes = [float(c[4]) for c in data.get('result', {}).get('list', [])]
        if len(closes) < 15:
            return None
        deltas = [closes[i + 1] - closes[i] for i in range(len(closes) - 1)]
        gains = [delta if delta > 0 else 0 for delta in deltas]
        losses = [-delta if delta < 0 else 0 for delta in deltas]

        avg_gain = sum(gains[-14:]) / 14
        avg_loss = sum(losses[-14:]) / 14
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi, 2)
    except Exception as e:
        return None

def send_telegram_alert(msg):
    bot.send_message(TELEGRAM_CHAT_ID, msg)

def main():
    send_telegram_alert("TEST: RSI Scanner für alle Bybit-Coins läuft stabil!")
    while True:
        symbols = get_spot_symbols()
        if not symbols:
            send_telegram_alert("Warnung: Konnte keine Bybit-Coins abrufen.")
        for symbol in symbols:
            rsi = get_rsi(symbol)
            if rsi is not None and rsi < 40:
                send_telegram_alert(f"{symbol}: RSI = {rsi} → Einstiegschance!")
        time.sleep(600)

if __name__ == "__main__":
    main()
