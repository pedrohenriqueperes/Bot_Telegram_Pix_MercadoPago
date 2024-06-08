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
    markup.add(button1, button2, button3)
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
