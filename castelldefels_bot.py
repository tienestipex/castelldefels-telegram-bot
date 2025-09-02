import time
import requests
from bs4 import BeautifulSoup

# Constantes de configuración
TELEGRAM_TOKEN = '7971079701:AAF-B-tD1nYQs5IuhuoBJTUKwBBBY7mXvgU'
CHAT_ID = '914909'
CHECK_INTERVAL = 5  # segundos

# URLs
URL_CASTELLDEFELS = 'https://www.castelldefels.org/ca/actualitat/elcastell/noticies'
URL_GAVA = 'https://www.gavaciutat.cat/es/actualitat/notes-de-premsa/'

# Variables para almacenar las últimas noticias detectadas
ultima_noticia_castelldefels = None
ultima_noticia_gava = None

def obtener_ultima_noticia_castelldefels():
    try:
        response = requests.get(URL_CASTELLDEFELS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        h2 = soup.find('h2', class_='newsItem__title h4 my-0')
        return h2.get_text(strip=True) if h2 else None
    except Exception as e:
        print(f"Error al obtener noticia de Castelldefels: {e}")
        return None

def obtener_ultima_noticia_gava():
    try:
        response = requests.get(URL_GAVA, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        h2 = soup.find('h2', class_='h3-size text-notransform mb-15 mt-0 mb-0')
        return h2.get_text(strip=True) if h2 else None
    except Exception as e:
        print(f"Error al obtener noticia de Gavà: {e}")
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
    global ultima_noticia_castelldefels, ultima_noticia_gava
    print("Bot vigilando Castelldefels y Gavà...")

    while True:
        # --- Castelldefels ---
        nueva_castelldefels = obtener_ultima_noticia_castelldefels()
        if nueva_castelldefels and nueva_castelldefels != ultima_noticia_castelldefels:
            ultima_noticia_castelldefels = nueva_castelldefels
            print(f"Nueva noticia en Castelldefels: {nueva_castelldefels}")
            enviar_telegram(f"🆕 Nova notícia de Castelldefels:\n\n<b>{nueva_castelldefels}</b>\n\n📍 {URL_CASTELLDEFELS}")

        # --- Gavà ---
        nueva_gava = obtener_ultima_noticia_gava()
        if nueva_gava and nueva_gava != ultima_noticia_gava:
            ultima_noticia_gava = nueva_gava
            print(f"Nueva noticia en Gavà: {nueva_gava}")
            enviar_telegram(f"🆕 Nova notícia de Gavà:\n\n<b>{nueva_gava}</b>\n\n📍 {URL_GAVA}")

        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
