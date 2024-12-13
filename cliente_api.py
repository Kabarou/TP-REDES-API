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

# Función para obtener premios por categoría
def obtener_premios_por_categoria(categoria):
    response = requests.get(f"{base_url}/prize/category/{categoria}")
    if response.status_code == 200:
        print(f"Premios en la categoría {categoria}:")
        pprint(response.json())
    else:
        print(f"Error al obtener premios en la categoría {categoria}: {response.status_code}")
        
        
# Función para agregar un nuevo premio
def agregar_premio(nuevo_premio):
    response = requests.post(f"{base_url}/prizes", json=nuevo_premio)
    if response.status_code == 200:
        print("Premio agregado exitosamente:")
        pprint(response.json())
    else:
        print(f"Error al agregar premio: {response.status_code}")


# Función para actualizar un premio por id de laureado
def actualizar_premio(laureate_id, premio_actualizado):
    response = requests.put(f"{base_url}/prize/{laureate_id}", json=premio_actualizado)
    if response.status_code == 200:
        print(f"Premio para el laureado con id {laureate_id} actualizado exitosamente:")
        pprint(response.json())
    else:
        print(f"Error al actualizar el premio: {response.status_code}")


# Función para eliminar un premio por año
def eliminar_premio(laureate_id):
    response = requests.delete(f"{base_url}/prize/laureate/{laureate_id}")
    if response.status_code == 200:
        print(f"Premio del laureado con ID {laureate_id} eliminado exitosamente.")
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

    # Obtener premios por categoría
    obtener_premios_por_categoria("chemistry")

    # Agregar un nuevo premio (Ejemplo)
    nuevo_premio = {
        "year": 2024,
        "category": "chemistry",
        "laureates": [
            {"id": 1, "firstname": "Marie", "surname": "Curie", "motivation": "For her work on radioactivity", "share": 1}
        ]
    }
    
    # Creamos un nuevo premio
    nuevo_premio = {
    "year": 2024, 
    "category": "literature",  
    "laureates": [
        {
            "id": 1,  
            "firstname": "Gabriel",  
            "surname": "Garcia Marquez",  
            "motivation": "Por su obra literaria, que ha elevado la literatura latinoamericana",  
            "share": 1  
        }
    ]
}
    # Llamamos al metodo para agregarlo
    agregar_premio(nuevo_premio)

    # Actualizar un premio por laureado (Ejemplo)
    premio_actualizado = {
        "year": 2020,
        "category": "chemistry",
        "laureates": [
            {"id": 1, "firstname": "Marie", "surname": "Curie", "motivation": "For her work on radioactivity", "share": 1},
            {"id": 2, "firstname": "Albert", "surname": "Einstein", "motivation": "For his work on relativity", "share": 1}
        ]
    }
    actualizar_premio(1, premio_actualizado)  # Usando el ID del laureado

    # Eliminar un premio por año
    eliminar_premio(1047)
"""

obtener_premios()

# Agregar menu interactivo