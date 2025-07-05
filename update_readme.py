import requests

USERNAME = "FamilyBoggart"  # <- reemplaza con tu nombre de usuario en CryptoHack
API_URL = f"https://cryptohack.org/api/user/{USERNAME}/"

response = requests.get(API_URL)
data = response.json()

score = data["score"]
rank = data["rank"]
total_users = data["user_count"]
username = data["username"]

nuevo_contenido = f"""\
- 👤 Usuario: {username}
- 🧠 Puntuación: {score} puntos
- 🥇 Ranking: {rank} / {total_users} usuarios
"""

# Leer README
with open("README.md", "r", encoding="utf-8") as file:
    contenido = file.read()

# Reemplazar sección entre marcadores
inicio = "<!--CRYPTOPROGRESS_START-->"
fin = "<!--CRYPTOPROGRESS_END-->"
seccion_vieja = contenido[contenido.find(inicio):contenido.find(fin)+len(fin)]
seccion_nueva = f"{inicio}\n{nuevo_contenido}\n{fin}"
contenido = contenido.replace(seccion_vieja, seccion_nueva)

# Guardar README actualizado
with open("README.md", "w", encoding="utf-8") as file:
    file.write(contenido)
