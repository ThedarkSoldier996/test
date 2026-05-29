import json
import requests

JSON_URL = "https://raw.githubusercontent.com/ThedarkSoldier996/test/refs/heads/main/novaplay.json"
SALIDA = "lista.m3u"

r = requests.get(JSON_URL)
r.raise_for_status()

data = r.text

# arregla JSON si viene sin []
if not data.strip().startswith("["):
    data = "[" + data + "]"

canales = json.loads(data)

with open(SALIDA, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")

    for c in canales:
        nombre = c.get("name", "Sin nombre")
        url = c.get("url", "")
        logo = c.get("icono", "")

        f.write(f'#EXTINF:-1 tvg-logo="{logo}",{nombre}\n')
        f.write(url + "\n")

print("M3U generado correctamente")
