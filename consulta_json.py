import requests
import json

# URL del JSON
url = "https://api.nobelprize.org/v1/prize.json"

# Descargamos el JSON
response = requests.get(url)
data = response.json()

# Guardamos en un archivo local
with open("prizes.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)

# Consultamos la cantidad de premios y categorías únicas
premios = data['prizes']
print(f"Total de premios: {len(premios)}")

categorias = {premio['category'] for premio in premios}
print(f"Categorías únicas: {categorias}")

# Ejemplo de consulta: premios en un año específico
year = "2020"
premios_2020 = [premio for premio in premios if premio['year'] == year]
print(f"Premios en {year}: {premios_2020}")
