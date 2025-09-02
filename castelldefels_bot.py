import time
import requests
from bs4 import BeautifulSoup

# Constantes de configuración
TELEGRAM_TOKEN = '7971079701:AAF-B-tD1nYQs5IuhuoBJTUKwBBBY7mXvgU'
CHAT_ID = '914909'
CHECK_INTERVAL = 5  # segundos

# URLs
URL_CASTELLDEFELS = 'https://www.castelldefels.org/ca/actualitat/elcastell/noticies'
URL_GAVA_PREMSA = 'https://www.gavaciutat.cat/es/actualitat/notes-de-premsa/'
URL_GAVA_ACTUALITAT = 'https://www.gavaciutat.cat/'

# Variables para almacenar las últimas noticias detectadas
ultima_noticia_castelldefels = None
ultima_noticia_gava_premsa = None
ultima_noticia_gava_actualitat = None

# --- Castelldefels ---
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

# --- Gavà: Notas de Premsa ---
def obtener_ultima_noticia_gava_premsa():
    try:
        response = requests.get(URL_GAVA_PREMSA, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        h2 = soup.find('h2', class_='h3-size text-notransform mb-15 mt-0 mb-0')
        return h2.get_text(strip=True) if h2 else None
    except Exception as e:
        print(f"Error al obtener noticia de Gavà (Premsa): {e}")
        return None

# --- Gavà: Actualitat ---
def obtener_ultima_noticia_gava_actualitat():
    try:
        response = requests.get(URL_GAVA_ACTUALITAT, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        h2 = soup.find('h2', class_='newsItem__title noTransformarText newsItemActualitat ')
        return h2.get_text(strip=True) if h2 else None
    except Exception as e:
        print(f"Error al obtener noticia de Gavà (Actualitat): {e}")
        return None

# --- Telegram ---
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

# --- Main ---
def main():
    global ultima_noticia_castelldefels, ultima_noticia_gava_premsa, ultima_noticia_gava_actualitat
    print("Bot vigilando Castelldefels y Gavà (2 apartados)...")

    while True:
        # Castelldefels
        nueva_castelldefels = obtener_ultima_noticia_castelldefels()
        if nueva_castelldefels and nueva_castelldefels != ultima_noticia_castelldefels:
            ultima_noticia_castelldefels = nueva_castelldefels
            print(f"Nueva noticia en Castelldefels: {nueva_castelldefels}")
            enviar_telegram(f"🆕 Nova notícia de Castelldefels:\n\n<b>{nueva_castelldefels}</b>\n\n📍 {URL_CASTELLDEFELS}")

        # Gavà – Notas de Premsa
        nueva_gava_premsa = obtener_ultima_noticia_gava_premsa()
        if nueva_gava_premsa and nueva_gava_premsa != ultima_noticia_gava_premsa:
            ultima_noticia_gava_premsa = nueva_gava_premsa
            print(f"Nueva noticia en Gavà (Premsa): {nueva_gava_premsa}")
            enviar_telegram(f"🆕 Nova notícia de Gavà (Notes de Premsa):\n\n<b>{nueva_gava_premsa}</b>\n\n📍 {URL_GAVA_PREMSA}")

        # Gavà – Actualitat
        nueva_gava_actualitat = obtener_ultima_noticia_gava_actualitat()
        if nueva_gava_actualitat and nueva_gava_actualitat != ultima_noticia_gava_actualitat:
            ultima_noticia_gava_actualitat = nueva_gava_actualitat
            print(f"Nueva noticia en Gavà (Actualitat): {nueva_gava_actualitat}")
            enviar_telegram(f"🆕 Nova notícia de Gavà (Actualitat):\n\n<b>{nueva_gava_actualitat}</b>\n\n📍 {URL_GAVA_ACTUALITAT}")

        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
