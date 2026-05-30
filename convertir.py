import json
import requests

JSON_URL = "https://raw.githubusercontent.com/ThedarkSoldier996/test/refs/heads/main/novaplay.json"
SALIDA = "lista.m3u"

BLOCKED_KEYWORDS = [
    "iframe", "dailymotion", "youtube", "embed",
    ".php", "player", "watch?", ".html"
]

VALID_EXTENSIONS = [
    ".m3u8",
    ".mpd"
]

def es_valido(url: str):
    if not url:
        return False

    url_lower = url.lower()

    # bloquear palabras malas
    for bad in BLOCKED_KEYWORDS:
        if bad in url_lower:
            return False

    # aceptar solo streams reales
    for ext in VALID_EXTENSIONS:
        if ext in url_lower:
            return True

    return False


r = requests.get(JSON_URL)
r.raise_for_status()

json_data = json.loads(r.text)

canales = []

for categoria in json_data:
    items = categoria.get("items", [])
    nombre_cat = categoria.get("title", "SIN CATEGORIA")

    for c in items:
        url = c.get("url", "")

        # 🔥 FILTRO PRINCIPAL
        if not es_valido(url):
            continue

        canales.append({
            "name": c.get("name") or "Sin nombre",
            "url": url,
            "logo": c.get("icono", ""),
            "group": nombre_cat
        })


with open(SALIDA, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")

    for c in canales:
        f.write(
            f'#EXTINF:-1 group-title="{c["group"]}" tvg-logo="{c["logo"]}",{c["name"]}\n'
        )
        f.write(c["url"] + "\n")

print("M3U generado sin iframe / PHP / embeds")
