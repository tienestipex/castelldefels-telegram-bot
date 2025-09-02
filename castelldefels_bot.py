import time
import requests
from bs4 import BeautifulSoup

# Configuración Telegram
TELEGRAM_TOKEN = '7971079701:AAF-B-tD1nYQs5IuhuoBJTUKwBBBY7mXvgU'
CHAT_ID = '914909'
CHECK_INTERVAL = 60  # segundos

# Lista de fuentes a vigilar
FUENTES = [
    {
        "nombre": "Castelldefels (Ajuntament)",
        "url": "https://www.castelldefels.org/ca/actualitat/elcastell/noticies",
        "selector": "h2.newsItem__title.h4.my-0 a",
        "base": "https://www.castelldefels.org"
    },
    {
        "nombre": "Gavà (Notes de Premsa)",
        "url": "https://www.gavaciutat.cat/es/actualitat/notes-de-premsa/",
        "selector": "h2.h3-size.text-notransform.mb-15.mt-0.mb-0 a",
        "base": "https://www.gavaciutat.cat"
    },
    {
        "nombre": "Gavà (Actualitat)",
        "url": "https://www.gavaciutat.cat/",
        "selector": "h2.newsItem__title.noTransformarText.newsItemActualitat a",
        "base": "https://www.gavaciutat.cat"
    },
    {
        "nombre": "Tauler Gavà",
        "url": "https://tauler.seu-e.cat/inici?idEns=808980001",
        "selector": "h2.MuiTypography-root.MuiTypography-h5.css-ywwhte a",
        "base": "https://tauler.seu-e.cat"
    },
    {
        "nombre": "Tauler Castelldefels",
        "url": "https://tauler.seu-e.cat/inici?idEns=805690004",
        "selector": "h2.MuiTypography-root.MuiTypography-h5.css-ywwhte a",
        "base": "https://tauler.seu-e.cat"
    },
    {
        "nombre": "Issuu Castelldefels",
        "url": "https://issuu.com/ajuntamentdecastelldefels",
        "selector": "h3.PublicationCard__publication-card__card-title__jufAN__0-0-3199 a",
        "base": "https://issuu.com"
    },
    {
        "nombre": "El Bruguers",
        "url": "https://elbruguersdigital.cat/",
        "selector": "h3.entry-title.td-module-title a",
        "base": "https://elbruguersdigital.cat"
    },
    {
        "nombre": "La Premsa del Baix - Gavà",
        "url": "https://www.lapremsadelbaix.es/poblacions/poblaciones-grupo-dos/gav%C3%A0.html?types%5B0%5D=1",
        "selector": "h2 a",
        "base": "https://www.lapremsadelbaix.es"
    },
    {
        "nombre": "La Premsa del Baix - Castelldefels",
        "url": "https://www.lapremsadelbaix.es/poblacions/poblaciones-grupo-uno/castelldefels.html?types%5B0%5D=1",
        "selector": "h2 a",
        "base": "https://www.lapremsadelbaix.es"
    },
    {
        "nombre": "El Periódico - Gavà",
        "url": "https://www.elperiodico.com/es/barcelona/gava/",
        "selector": "h2.ft-org-cardHome__mainTitle a",
        "base": "https://www.elperiodico.com"
    },
    {
        "nombre": "El Periódico - Castelldefels",
        "url": "https://www.elperiodico.com/es/barcelona/castelldefels/",
        "selector": "h2.ft-org-cardHome__mainTitle a",
        "base": "https://www.elperiodico.com"
    }
]

# Diccionario para guardar últimas noticias
ultimas_noticias = {fuente["nombre"]: None for fuente in FUENTES}

# --- Función genérica para obtener noticia ---
def obtener_ultima_noticia(fuente):
    try:
        response = requests.get(fuente["url"], timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        noticia = soup.select_one(fuente["selector"])
        if noticia:
            titulo = noticia.get_text(strip=True)
            enlace = noticia["href"] if noticia.has_attr("href") else fuente["url"]
            if not enlace.startswith("http"):
                enlace = fuente["base"] + enlace
            return titulo, enlace
        return None
    except Exception as e:
        print(f"Error al obtener noticia de {fuente['nombre']}: {e}")
        return None

# --- Enviar Telegram ---
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

# --- Main loop ---
def main():
    print("Bot vigilando múltiples fuentes de noticias...")
    global ultimas_noticias

    while True:
        for fuente in FUENTES:
            nueva = obtener_ultima_noticia(fuente)
            if nueva and nueva != ultimas_noticias[fuente["nombre"]]:
                ultimas_noticias[fuente["nombre"]] = nueva
                titulo, enlace = nueva
                print(f"🆕 Nueva noticia en {fuente['nombre']}: {titulo}")
                enviar_telegram(f"🆕 Nova notícia de <b>{fuente['nombre']}</b>:\n\n<b>{titulo}</b>\n\n🔗 {enlace}")
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
