
import requests
import time
import hmac
import hashlib
import time
import json
import telebot

# === Benutzer-Zugangsdaten (bitte ersetzen) ===
API_KEY = 'udRZsZ1NQ0ELK0PSrS'
API_SECRET = 'bAjlUEKQBTBvdsHgs5lvy6VRX94b4xaT1Xoj'
TELEGRAM_BOT_TOKEN = '8047247430:AAHz-YvXSnhkxgdPOzbeXP81PZFz4llgvTM'
TELEGRAM_CHAT_ID = 7465646426

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def get_rsi(symbol='PEPEUSDT', interval='1h', limit=200):
    url = f"https://api.bybit.com/v5/market/kline?category=spot&symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()

    if 'result' not in data or 'list' not in data['result']:
        return None

    closes = [float(c[4]) for c in data['result']['list']]  # Schlusskurse
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

def send_telegram_alert(msg):
    bot.send_message(TELEGRAM_CHAT_ID, msg)

def main():
    send_telegram_alert('TEST-ALARM: Dein Bot läuft erfolgreich und ist aktiv!')
    while True:
        rsi = get_rsi()
        if rsi is not None and rsi < 30:
            send_telegram_alert(f"RSI bei PEPE/USDT = {rsi} → Einstiegschance!")
        time.sleep(600)  # alle 10 Minuten prüfen

if __name__ == "__main__":
    main()
