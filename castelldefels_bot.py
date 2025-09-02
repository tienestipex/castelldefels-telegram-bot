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

URL_PREMSA_GAVA = 'https://www.lapremsadelbaix.es/poblacions/poblaciones-grupo-dos/gav%C3%A0.html?types%5B0%5D=1'
URL_PREMSA_CASTELLDEFELS = 'https://www.lapremsadelbaix.es/poblacions/poblaciones-grupo-uno/castelldefels.html?types%5B0%5D=1'
URL_PERIODICO_GAVA = 'https://www.elperiodico.com/es/barcelona/gava/'
URL_PERIODICO_CASTELLDEFELS = 'https://www.elperiodico.com/es/barcelona/castelldefels/'

# Variables para almacenar las últimas noticias detectadas
ultima_noticia_castelldefels = None
ultima_noticia_gava_premsa = None
ultima_noticia_gava_actualitat = None
ultima_noticia_premsa_gava = None
ultima_noticia_premsa_castelldefels = None
ultima_noticia_periodico_gava = None
ultima_noticia_periodico_castelldefels = None

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

# --- La Premsa del Baix: Gavà ---
def obtener_ultima_noticia_premsa_gava():
    try:
        response = requests.get(URL_PREMSA_GAVA, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        noticia = soup.find('h2')
        if noticia and noticia.a:
            titulo = noticia.get_text(strip=True)
            enlace = noticia.a['href']
            if not enlace.startswith("http"):
                enlace = "https://www.lapremsadelbaix.es" + enlace
            return titulo, enlace
        return None
    except Exception as e:
        print(f"Error al obtener noticia de La Premsa (Gavà): {e}")
        return None

# --- La Premsa del Baix: Castelldefels ---
def obtener_ultima_noticia_premsa_castelldefels():
    try:
        response = requests.get(URL_PREMSA_CASTELLDEFELS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        noticia = soup.find('h2')
        if noticia and noticia.a:
            titulo = noticia.get_text(strip=True)
            enlace = noticia.a['href']
            if not enlace.startswith("http"):
                enlace = "https://www.lapremsadelbaix.es" + enlace
            return titulo, enlace
        return None
    except Exception as e:
        print(f"Error al obtener noticia de La Premsa (Castelldefels): {e}")
        return None

# --- El Periódico: Gavà ---
def obtener_ultima_noticia_periodico_gava():
    try:
        response = requests.get(URL_PERIODICO_GAVA, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        noticia = soup.find('h2', class_='ft-org-cardHome__mainTitle')
        if noticia and noticia.a:
            titulo = noticia.get_text(strip=True)
            enlace = noticia.a['href']
            if not enlace.startswith("http"):
                enlace = "https://www.elperiodico.com" + enlace
            return titulo, enlace
        return None
    except Exception as e:
        print(f"Error al obtener noticia de El Periódico (Gavà): {e}")
        return None

# --- El Periódico: Castelldefels ---
def obtener_ultima_noticia_periodico_castelldefels():
    try:
        response = requests.get(URL_PERIODICO_CASTELLDEFELS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        noticia = soup.find('h2', class_='ft-org-cardHome__mainTitle')
        if noticia and noticia.a:
            titulo = noticia.get_text(strip=True)
            enlace = noticia.a['href']
            if not enlace.startswith("http"):
                enlace = "https://www.elperiodico.com" + enlace
            return titulo, enlace
        return None
    except Exception as e:
        print(f"Error al obtener noticia de El Periódico (Castelldefels): {e}")
        return None

# --- Telegram ---
def enviar_telegram(mensaje):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': mensaje,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True  # 👈 evita carátula/imagen previa
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error al enviar mensaje de Telegram: {e}")

# --- Main ---
def main():
    global ultima_noticia_castelldefels, ultima_noticia_gava_premsa, ultima_noticia_gava_actualitat
    global ultima_noticia_premsa_gava, ultima_noticia_premsa_castelldefels
    global ultima_noticia_periodico_gava, ultima_noticia_periodico_castelldefels

    print("Bot vigilando Castelldefels y Gavà en múltiples medios...")

    while True:
        # Castelldefels
        nueva_castelldefels = obtener_ultima_noticia_castelldefels()
        if nueva_castelldefels and nueva_castelldefels != ultima_noticia_castelldefels:
            ultima_noticia_castelldefels = nueva_castelldefels
            titulo, enlace = nueva_castelldefels
            enviar_telegram(f"🔵 Nueva noticia de Castelldefels (Ayuntamiento):\n\n<b>{titulo}</b>\n\n🔗 <a href='{enlace}'>Ver más</a>")

        # Gavà – Notas de Premsa
        nueva_gava_premsa = obtener_ultima_noticia_gava_premsa()
        if nueva_gava_premsa and nueva_gava_premsa != ultima_noticia_gava_premsa:
            ultima_noticia_gava_premsa = nueva_gava_premsa
            titulo, enlace = nueva_gava_premsa
            enviar_telegram(f"🟢 Nueva noticia de Gavà (Nota de prensa):\n\n<b>{titulo}</b>\n\n🔗 <a href='{enlace}'>Ver más</a>")

        # Gavà – Actualitat
        nueva_gava_actualitat = obtener_ultima_noticia_gava_actualitat()
        if nueva_gava_actualitat and nueva_gava_actualitat != ultima_noticia_gava_actualitat:
            ultima_noticia_gava_actualitat = nueva_gava_actualitat
            titulo, enlace = nueva_gava_actualitat
            enviar_telegram(f"🟢 Nueva noticia de Gavà (Actualidad):\n\n<b>{titulo}</b>\n\n🔗 <a href='{enlace}'>Ver más</a>")

        # La Premsa – Gavà
        nueva_premsa_gava = obtener_ultima_noticia_premsa_gava()
        if nueva_premsa_gava and nueva_premsa_gava != ultima_noticia_premsa_gava:
            ultima_noticia_premsa_gava = nueva_premsa_gava
            titulo, enlace = nueva_premsa_gava
            enviar_telegram(f"🟢 Nova notícia de La Premsa del Baix (Gavà):\n\n<b>{titulo}</b>\n\n🔗 <a href='{enlace}'>Ver más</a>")

        # La Premsa – Castelldefels
        nueva_premsa_castelldefels = obtener_ultima_noticia_premsa_castelldefels()
        if nueva_premsa_castelldefels and nueva_premsa_castelldefels != ultima_noticia_premsa_castelldefels:
            ultima_noticia_premsa_castelldefels = nueva_premsa_castelldefels
            titulo, enlace = nueva_premsa_castelldefels
            enviar_telegram(f"🔵 Nueva noticia de La Premsa del Baix (Castelldefels):\n\n<b>{titulo}</b>\n\n🔗 <a href='{enlace}'>Ver más</a>")

        # El Periódico – Gavà
        nueva_periodico_gava = obtener_ultima_noticia_periodico_gava()
        if nueva_periodico_gava and nueva_periodico_gava != ultima_noticia_periodico_gava:
            ultima_noticia_periodico_gava = nueva_periodico_gava
            titulo, enlace = nueva_periodico_gava
            enviar_telegram(f"🟢 Nueva noticia de El Periódico (Gavà):\n\n<b>{titulo}</b>\n\n🔗 <a href='{enlace}'>Ver más</a>")

        # El Periódico – Castelldefels
        nueva_periodico_castelldefels = obtener_ultima_noticia_periodico_castelldefels()
        if nueva_periodico_castelldefels and nueva_periodico_castelldefels != ultima_noticia_periodico_castelldefels:
            ultima_noticia_periodico_castelldefels = nueva_periodico_castelldefels
            titulo, enlace = nueva_periodico_castelldefels
            enviar_telegram(f"🔵 Nueva noticia de El Periódico (Castelldefels):\n\n<b>{titulo}</b>\n\n🔗 <a href='{enlace}'>Ver más</a>")

        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
