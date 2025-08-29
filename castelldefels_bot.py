import time
import requests
from bs4 import BeautifulSoup

# Constantes de configuración
TELEGRAM_TOKEN = '7971079701:AAF-B-tD1nYQs5IuhuoBJTUKwBBBY7mXvgU'
CHAT_ID = '914909'
CHECK_INTERVAL = 5  # segundos
URL = 'https://www.castelldefels.org/ca/actualitat/elcastell/noticies'
URL2 = 'https://contractaciopublica.cat/ca/cerca-avancada?page=0&filtreText=Castelldefels&inclourePublicacionsPlacsp=false&sortField=dataUltimaPublicacio&sortOrder=desc'
BASE_URL2 = 'https://contractaciopublica.cat'

# Variables para almacenar las últimas noticias detectadas
ultima_noticia = None
ultima_noticia_contractacio = None

def obtener_ultima_noticia():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        h2 = soup.find('h2', class_='newsItem__title h4 my-0')
        return h2.get_text(strip=True) if h2 else None
    except Exception as e:
        print(f"Error al obtener la noticia de Castelldefels.org: {e}")
        return None

def obtener_ultima_noticia_contractacio():
    try:
        response = requests.get(URL2, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        a_tag = soup.find('a', class_='fw-bold text-black text-decoration-none fs-4')
        if a_tag:
            titulo = a_tag.get_text(strip=True)
            enlace = BASE_URL2 + a_tag['href']
            return titulo, enlace
        return None, None
    except Exception as e:
        print(f"Error al obtener la noticia de Contractació Pública: {e}")
        return None, None

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
    global ultima_noticia, ultima_noticia_contractacio
    print("Bot vigilando Castelldefels.org y Contractaciopublica.cat...")
    while True:
        # Castelldefels.org
        nueva_noticia = obtener_ultima_noticia()
        if nueva_noticia and nueva_noticia != ultima_noticia:
            ultima_noticia = nueva_noticia
            print(f"Nueva noticia detectada en Castelldefels.org: {nueva_noticia}")
            enviar_telegram(f"🆕 Nova notícia de Castelldefels.org:\n\n<b>{nueva_noticia}</b>\n\n📍 {URL}")

        # Contractaciopublica.cat
        nueva_noticia_contractacio, enlace_contractacio = obtener_ultima_noticia_contractacio()
        if nueva_noticia_contractacio and nueva_noticia_contractacio != ultima_noticia_contractacio:
            ultima_noticia_contractacio = nueva_noticia_contractacio
            print(f"Nova publicació detectada a Contractació Pública: {nueva_noticia_contractacio}")
            enviar_telegram(f"📑 Nova publicació de Contractació Pública:\n\n<b>{nueva_noticia_contractacio}</b>\n\n🔗 {enlace_contractacio}")

        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
