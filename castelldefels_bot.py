
import time
import requests
from bs4 import BeautifulSoup

# Constantes de configuración
TELEGRAM_TOKEN = '7971079701:AAF-B-tD1nYQs5IuhuoBJTUKwBBBY7mXvgU'
CHAT_ID = '914909'
CHECK_INTERVAL = 5  # segundos
URL = 'https://www.castelldefels.org/ca/actualitat/elcastell/noticies'

# Variable para almacenar la última noticia detectada
ultima_noticia = None

def obtener_ultima_noticia():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        h2 = soup.find('h2', class_='newsItem__title h4 my-0')
        return h2.get_text(strip=True) if h2 else None
    except Exception as e:
        print(f"Error al obtener la noticia: {e}")
        return None

def enviar_telegram(mensaje):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': mensaje,
        'parse_mode': 'HTML'
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error al enviar mensaje de Telegram: {e}")

def main():
    global ultima_noticia
    print("Bot vigilando Castelldefels.org...")
    while True:
        nueva_noticia = obtener_ultima_noticia()
        if nueva_noticia and nueva_noticia != ultima_noticia:
            ultima_noticia = nueva_noticia
            print(f"Nueva noticia detectada: {nueva_noticia}")
            enviar_telegram(f"🆕 Nova notícia de Castelldefels:\n\n<b>{nueva_noticia}</b>\n\n📍 {URL}")
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
