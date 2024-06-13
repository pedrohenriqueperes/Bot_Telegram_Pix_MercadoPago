
# Telegram Payment Bot

This is a simple Telegram bot that offers users different subscription plans and generates a PIX payment code for the selected plan. The bot uses the TeleBot library for handling Telegram messages and callbacks.

## Features

- Presents users with a choice of three subscription plans.
- Generates a PIX payment code for the selected plan.
- Sends the PIX payment code to the user via Telegram.

## Requirements

- Python 3.7+
- TeleBot library
- Requests library
- Dotenv library

## Setup

1. Clone this repository or copy the code to your local machine.
2. Install the required libraries using pip:
    ```bash
    pip install pytelegrambotapi requests python-dotenv
    ```
3. Create a `.env` file in the same directory as the script and add your Telegram bot API key:
    ```env
    BOT_API=your_telegram_bot_api_key
    ```
4. Make sure you have a running Flask application that generates PIX payment codes. The Flask app should have an endpoint `/get_payment` that accepts a JSON payload with `price` and `description` and returns a JSON response with the PIX code in the `clipboard` field.

## Usage

1. Start the Telegram bot by running the script:
    ```bash
    python bot.py
    ```
2. In Telegram, start a chat with your bot and send the `/start` command.
3. Choose one of the presented subscription plans.
4. The bot will generate and send you a PIX payment code for the selected plan.

## Code Overview

```python
from telebot import TeleBot, types
import os
from dotenv import load_dotenv

load_dotenv()

bot = TeleBot(str(os.getenv('BOT_API')))

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Plano 1 - R$100", callback_data='plano_1')
    button2 = types.InlineKeyboardButton("Plano 2 - R$200", callback_data='plano_2')
    button3 = types.InlineKeyboardButton("Plano 3 - R$300", callback_data='plano_3')
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    bot.send_message(message.chat.id, "Escolha um plano:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'plano_1':
        price = 100.0
        description = "Plano 1"
    elif call.data == 'plano_2':
        price = 200.0
        description = "Plano 2"
    elif call.data == 'plano_3':
        price = 300.0
        description = "Plano 3"
    else:
        return

    generate_payment(call.message, price, description)

def generate_payment(message, price, description):
    import requests
    url = "http://127.0.0.1:5000/get_payment"
    payload = {
        "price": price,
        "description": description
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        pix_code = data['clipboard']
        bot.send_message(message.chat.id, f"Código PIX para pagamento:")
        bot.send_message(message.chat.id, f"\n{pix_code}")
    else:
        bot.send_message(message.chat.id, "Erro ao gerar o código de pagamento. Tente novamente mais tarde.")

bot.polling()
```

## Notes

- Ensure your Flask application is running and accessible at the specified URL (`http://127.0.0.1:5000`).
- Customize the subscription plans and prices as needed.
- You may need to adjust the PIX payment generation logic based on your specific implementation and requirements.

## License

This project is licensed under the MIT License.
