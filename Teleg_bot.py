"""Telegram бот @https://t.me/big_NLP_bot"""

from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests
TOKEN = "7065854119:AAE0FI4Yc1TA3TcvMmhxe4qe0TVDTZExXqw"
CRYPTO_NAME_TO_TICKER = {
    "Bitcoin": "BTCUSDT",
    "Ethereum": "ETHUSDT",
    "BNB": "BNBUSDT",
    "Solana": "SOLUSDT",
    "Cardana": "ADAUSDT",
    "Dogecoin": "DOGEUSDT"}

bot = TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(row_width=6)
    for crypto_name in CRYPTO_NAME_TO_TICKER.keys():
        item_button = KeyboardButton(crypto_name)
        markup.add(item_button)
    bot.send_message(message.chat.id, "Бот от Александр Викторовича", reply_markup=markup)
    bot.send_message(message.chat.id, "Выбирите крипту", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in CRYPTO_NAME_TO_TICKER.keys())
def send_price(message):
    crypto_name = message.text
    ticker = CRYPTO_NAME_TO_TICKER[crypto_name]
    price = get_price_by_ticker(ticker=ticker)
    print(crypto_name)
    print(price)
    bot.send_message(message.chat.id, f"Цена {crypto_name} равна {price} USDT")

def get_price_by_ticker(ticker: str):
    endpoint = "https://api.binance.com/api/v3/ticker/price"
    params = {
        'symbol': ticker,
    }
    response = requests.get(endpoint, params=params)
    data = response.json()
    price = round(float(data["price"]), 2)
    return price

bot.infinity_polling()