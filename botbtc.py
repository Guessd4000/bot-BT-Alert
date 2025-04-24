import requests
import matplotlib.pyplot as plt
import pandas as pd
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import time

# Suas chaves de API
TELEGRAM_API_KEY = '7757204285:AAH1cKohAVRBcIHEEV7h7bCLnefn5hNyk44'
COINMARKETCAP_API_KEY = 'adc709da-b834-48b8-95c4-e9f5da9debae'

# Função para obter o preço do Bitcoin
def get_bitcoin_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '10',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
    }
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()
    bitcoin_data = data['data'][0]
    return bitcoin_data['quote']['USD']['price'], bitcoin_data['quote']['USD']['volume_24h']

# Função para gerar um gráfico simples
def generate_chart():
    data = pd.DataFrame({
        'Time': ['T1', 'T2', 'T3', 'T4', 'T5'],
        'Price': [40000, 40500, 41000, 39500, 42000]
    })
    plt.plot(data['Time'], data['Price'])
    plt.title('Preço do Bitcoin')
    plt.xlabel('Tempo')
    plt.ylabel('Preço em USD')
    plt.savefig('bitcoin_price.png')

# Função de alerta
def send_alert(update: Update, context: CallbackContext):
    price, volume = get_bitcoin_price()
    alert_msg = f'Preço do Bitcoin: ${price}\nVolume de 24h: ${volume}'
    
    # Alerta de variação de preço
    if price >= 1200:  # Você pode comparar com o preço atual para saber quando o Bitcoin subiu ou desceu 1200 USD
        alert_msg += '\nAlerta: O Bitcoin subiu 1200 USD!'
    
    # Alerta de volume
    if volume >= 200000000:
        alert_msg += '\nAlerta: O volume de 24h passou de 200 milhões!'
    
    context.bot.send_message(chat_id=update.message.chat_id, text=alert_msg)
    
    # Gerar e enviar gráfico
    generate_chart()
    context.bot.send_photo(chat_id=update.message.chat_id, photo=open('bitcoin_price.png', 'rb'))

# Função de comando para iniciar o bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Bot de monitoramento de Bitcoin iniciado!')

# Configuração do bot
def main():
    updater = Updater(TELEGRAM_API_KEY, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('alert', send_alert))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
