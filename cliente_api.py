import requests
from pprint import pprint

# URL del servidor API
base_url = "http://localhost:8000"  


# Función para obtener todos los premios
def obtener_premios():
    response = requests.get(f"{base_url}/prizes")
    if response.status_code == 200:
        print("Premios obtenidos exitosamente:")
        pprint(response.json())
    else:
        print(f"Error al obtener premios: {response.status_code}")


# Función para obtener premios por año
def obtener_premios_por_anio(anio):
    response = requests.get(f"{base_url}/prize/{anio}")
    if response.status_code == 200:
        print(f"Premios del año {anio}:")
        pprint(response.json())
    else:
        print(f"Error al obtener premios del año {anio}: {response.status_code}")


# Función para agregar un nuevo premio
def agregar_premio(nuevo_premio):
    response = requests.post(f"{base_url}/prizes", json=nuevo_premio)
    if response.status_code == 200:
        print("Premio agregado exitosamente:")
        pprint(response.json())
    else:
        print(f"Error al agregar premio: {response.status_code}")


# Función para actualizar un premio por año
def actualizar_premio(anio, premio_actualizado):
    response = requests.put(f"{base_url}/prize/{anio}", json=premio_actualizado)
    if response.status_code == 200:
        print(f"Premio del año {anio} actualizado exitosamente:")
        pprint(response.json())
    else:
        print(f"Error al actualizar el premio: {response.status_code}")


# Función para actualizar premios por categoría
def actualizar_premios_por_categoria(categoria, premio_actualizado):
    response = requests.put(f"{base_url}/prize/category/{categoria}", json=premio_actualizado)
    if response.status_code == 200:
        print(f"Premios en la categoría {categoria} actualizados exitosamente:")
        pprint(response.json())
    else:
        print(f"Error al actualizar premios de la categoría {categoria}: {response.status_code}")


# Función para eliminar un premio por año
def eliminar_premio(anio):
    response = requests.delete(f"{base_url}/prize/{anio}")
    if response.status_code == 200:
        print(f"Premio del año {anio} eliminado exitosamente.")
    else:
        print(f"Error al eliminar el premio: {response.status_code}")



"""""
# Ejemplo de cómo llamar a las funciones
if __name__ == "__main__":
    # Llamar a cada función según el caso que desees probar

    # Obtener todos los premios
    obtener_premios()

    # Obtener premios por año
    obtener_premios_por_anio(2020)

    # Agregar un nuevo premio (Ejemplo)
    nuevo_premio = {
        "year": 2024,
        "category": "chemistry",
        "laureates": [
            {"id": 1, "firstname": "Marie", "surname": "Curie"}
        ]
    }
    agregar_premio(nuevo_premio)

    # Actualizar un premio por año (Ejemplo)
    premio_actualizado = {
        "year": 2020,
        "category": "chemistry",
        "laureates": [
            {"id": 1, "firstname": "Marie", "surname": "Curie"},
            {"id": 2, "firstname": "Albert", "surname": "Einstein"}
        ]
    }
    actualizar_premio(2020, premio_actualizado)

    # Eliminar un premio por año
    eliminar_premio(2020)

    # Actualizar premios por categoría
    premio_actualizado_categoria = {
        "year": 2024,
        "category": "chemistry",
        "laureates": [
            {"id": 1, "firstname": "Marie", "surname": "Curie"}
        ]
    }
    actualizar_premios_por_categoria("chemistry", premio_actualizado_categoria)
"""

obtener_premios()

# Agregar menu interactivo