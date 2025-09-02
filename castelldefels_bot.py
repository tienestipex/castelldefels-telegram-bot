import time
import requests
from bs4 import BeautifulSoup

# Constantes de configuración
TELEGRAM_TOKEN = '7971079701:AAF-B-tD1nYQs5IuhuoBJTUKwBBBY7mXvgU'
CHAT_ID = '914909'
CHECK_INTERVAL = 30  # segundos

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
        noticia = soup.find('h2', class_='newsItem__title h4 my-0')
        if noticia and noticia.a:
            titulo = noticia.get_text(strip=True)
            enlace = noticia.a['href']
            if not enlace.startswith("http"):
                enlace = "https://www.castelldefels.org" + enlace
            return titulo, enlace
        return None
    except Exception as e:
        print(f"Error al obtener noticia de Castelldefels: {e}")
        return None

# --- Gavà: Notas de Premsa ---
def obtener_ultima_noticia_gava_premsa():
    try:
        response = requests.get(URL_GAVA_PREMSA, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        noticia = soup.find('h2', class_='h3-size text-notransform mb-15 mt-0 mb-0')
        if noticia and noticia.a:
            titulo = noticia.get_text(strip=True)
            enlace = noticia.a['href']
            if not enlace.startswith("http"):
                enlace = "https://www.gavaciutat.cat" + enlace
            return titulo, enlace
        return None
    except Exception as e:
        print(f"Error al obtener noticia de Gavà (Premsa): {e}")
        return None

# --- Gavà: Actualitat ---
def obtener_ultima_noticia_gava_actualitat():
    try:
        response = requests.get(URL_GAVA_ACTUALITAT, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        noticia = soup.select_one("h2.newsItem__title.noTransformarText.newsItemActualitat")
        if noticia and noticia.a:
            titulo = noticia.get_text(strip=True)
            enlace = noticia.a['href']
            if not enlace.startswith("http"):
                enlace = "https://www.gavaciutat.cat" + enlace
            return titulo, enlace
        return None
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
            titulo, enlace = nueva_castelldefels
            print(f"Nueva noticia en Castelldefels: {titulo}")
            enviar_telegram(f"🆕 Nova notícia de Castelldefels:\n\n<b>{titulo}</b>\n\n🔗 {enlace}")

        # Gavà – Notas de Premsa
        nueva_gava_premsa = obtener_ultima_noticia_gava_premsa()
        if nueva_gava_premsa and nueva_gava_premsa != ultima_noticia_gava_premsa:
            ultima_noticia_gava_premsa = nueva_gava_premsa
            titulo, enlace = nueva_gava_premsa
            print(f"Nueva noticia en Gavà (Premsa): {titulo}")
            enviar_telegram(f"🆕 Nova notícia de Gavà (Notes de Premsa):\n\n<b>{titulo}</b>\n\n🔗 {enlace}")

        # Gavà – Actualitat
        nueva_gava_actualitat = obtener_ultima_noticia_gava_actualitat()
        if nueva_gava_actualitat and nueva_gava_actualitat != ultima_noticia_gava_actualitat:
            ultima_noticia_gava_actualitat = nueva_gava_actualitat
            titulo, enlace = nueva_gava_actualitat
            print(f"Nueva noticia en Gavà (Actualitat): {titulo}")
            enviar_telegram(f"🆕 Nova notícia de Gavà (Actualitat):\n\n<b>{titulo}</b>\n\n🔗 {enlace}")

        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
