import requests

BOT_TOKEN = '8151420176:AAGDeiToWhTUTppBX1tq3H2smj6C6AdTdag'  # replace with your token
CHAT_ID = '1892670413'  # replace with your Telegram ID
NEWS_TEXT = "📰 Today's Top News:\n\n1. Example News Headline\n2. Another headline..."

def send_telegram_message():
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': CHAT_ID,
        'text': NEWS_TEXT
    }
    response = requests.post(url, data=data)
    print("Message status:", response.json())

send_telegram_message()
