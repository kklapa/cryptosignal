import requests
import telebot
import time
import threading

# Встав свій токен від BotFather
TOKEN = "7471047075:AAHbB8p-jaduRNr-gs-JB6LkJPYHQJUZef4"
bot = telebot.TeleBot(TOKEN)

# Список криптовалют та поріг зміни ціни
COINS = ["bitcoin", "ethereum", "gatechain-token", "solana"]
CURRENCY = "usd"
THRESHOLD = 2.0  # % зміни для сигналу

last_prices = {coin: None for coin in COINS}
YOUR_CHAT_ID = "824229409"  # Замінити на свій chat_id

# Функція отримання цін з CoinGecko
def get_prices():
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(COINS)}&vs_currencies={CURRENCY}"
    response = requests.get(url)
    return response.json()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привіт! Я бот для відстеження криптовалют. Я повідомлю, коли варто купувати або продавати.")

def check_prices():
    global last_prices
    prices = get_prices()
    for coin in COINS:
        price = prices.get(coin, {}).get(CURRENCY)
        if price and last_prices[coin]:
            change = ((price - last_prices[coin]) / last_prices[coin]) * 100
            if change >= THRESHOLD:
                bot.send_message(YOUR_CHAT_ID, f'🚀 {coin.upper()} зросла на {change:.2f}%. Поточна ціна: {price:.2f} USD. Час продавати!')
            elif change <= -THRESHOLD:
                bot.send_message(YOUR_CHAT_ID, f'📉 {coin.upper()} впала на {change:.2f}%. Поточна ціна: {price:.2f} USD. Час купувати!')
        last_prices[coin] = price

# Функція для періодичного запуску перевірки цін
def price_check_loop():
    while True:
        check_prices()
        time.sleep(60)  # Перевірка кожну хвилину

if __name__ == "__main__":
    # Запуск перевірки цін у окремому потоці
    threading.Thread(target=price_check_loop, daemon=True).start()
    bot.polling(none_stop=True)
