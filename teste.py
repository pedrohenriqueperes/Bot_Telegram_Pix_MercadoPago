from telebot import TeleBot, types
import os
import requests
from dotenv import load_dotenv

load_dotenv()

bot = TeleBot(str(os.getenv('BOT_API')))

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Plano 1 - R$1", callback_data='plano_1')
    button2 = types.InlineKeyboardButton("Plano 2 - R$2", callback_data='plano_2')
    button3 = types.InlineKeyboardButton("Plano 3 - R$3", callback_data='plano_3')
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    bot.send_message(message.chat.id, "Escolha um plano:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'plano_1':
        price = 1.0
        description = "Plano 1"
    elif call.data == 'plano_2':
        price = 2.0
        description = "Plano 2"
    elif call.data == 'plano_3':
        price = 3.0
        description = "Plano 3"
    else:
        return

    generate_payment(call.message, price, description)

def generate_payment(message, price, description):
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
        markup = types.InlineKeyboardMarkup()
        confirm_button = types.InlineKeyboardButton("Confirmar Pagamento", callback_data=f"confirm_payment_{data['id']}")
        markup.add(confirm_button)
        bot.send_message(message.chat.id, "Por favor, confirme o pagamento clicando no botão abaixo:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Erro ao gerar o código de pagamento. Tente novamente mais tarde.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_payment'))
def handle_confirmation(call):
    print("Callback received:", call.data)
    payment_id = call.data.split('_')[1]
    print("Payment ID:", payment_id)
    confirm_payment_request(call.message, payment_id)

def confirm_payment_request(message, payment_id):
    print("Verifying payment:", payment_id)
    url = "http://127.0.0.1:5000/verify_payment"
    payload = {
        "id": payment_id
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'approved':
            bot.send_message(message.chat.id, "Pagamento confirmado com sucesso!")
        else:
            bot.send_message(message.chat.id, "Pagamento ainda não foi aprovado. Verifique novamente mais tarde.")
    else:
        bot.send_message(message.chat.id, "Erro ao verificar o pagamento. Tente novamente mais tarde.")

bot.polling()
