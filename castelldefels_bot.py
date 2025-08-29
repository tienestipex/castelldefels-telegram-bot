import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin  # ⬅️ para construir el enlace absoluto

# Constantes de configuración
TELEGRAM_TOKEN = '7971079701:AAF-B-tD1nYQs5IuhuoBJTUKwBBBY7mXvgU'
CHAT_ID = '914909'
CHECK_INTERVAL = 5  # segundos
URL = 'https://www.castelldefels.org/ca/actualitat/elcastell/noticies'
URL2 = ('https://contractaciopublica.cat/ca/cerca-avancada?page=0'
        '&filtreText=Castelldefels&inclourePublicacionsPlacsp=false'
        '&sortField=dataUltimaPublicacio&sortOrder=desc')
BASE_URL2 = 'https://contractaciopublica.cat'

# Cabeceras para evitar bloqueos por parte del sitio
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'ca,es-ES;q=0.9,es;q=0.8,en;q=0.7',
}

# Variables para almacenar las últimas noticias detectadas
ultima_noticia = None
ultima_noticia_contractacio = None

def obtener_ultima_noticia():
    try:
        # (opcional) también podríamos pasar HEADERS aquí, pero lo dejo igual para no tocar lo que ya funcionaba
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
        # Usamos cabeceras y un selector robusto por patrón de href
        response = requests.get(URL2, timeout=15, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1) Selector robusto: primer <a> cuyo href empiece por /ca/detall-publicacio/
        a_tag = soup.select_one('a[href^="/ca/detall-publicacio/"]')

        # 2) Fallback por clases (por si cambia la estructura del HTML)
        if not a_tag:
            a_tag = soup.select_one('a.fw-bold.text-black.text-decoration-none.fs-4')

        if a_tag and a_tag.get('href'):
            titulo = a_tag.get_text(strip=True)
            enlace = urljoin(BASE_URL2, a_tag['href'])
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
        requests.post(url, data=payload, timeout=10)
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
            enviar_telegram(f"📰 Nova notícia de Castelldefels.org:\n\n<b>{nueva_noticia}</b>\n\n📍 {URL}")

        # Contractaciopublica.cat
        nueva_noticia_contractacio, enlace_contractacio = obtener_ultima_noticia_contractacio()
        if nueva_noticia_contractacio and nueva_noticia_contractacio != ultima_noticia_contractacio:
            ultima_noticia_contractacio = nueva_noticia_contractacio
            print(f"Nova publicació detectada a Contractació Pública: {nueva_noticia_contractacio}")
            enviar_telegram(
                f"📑 Nova publicació de Contractació Pública:\n\n"
                f"<b>{nueva_noticia_contractacio}</b>\n\n🔗 {enlace_contractacio}"
            )

        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
