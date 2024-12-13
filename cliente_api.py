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
def obtener_premios_por_anio():
    anio = int(input("Ingrese un año: "))
    response = requests.get(f"{base_url}/prize/{anio}")
    if response.status_code == 200:
        print(f"Premios del año {anio}:")
        pprint(response.json())
    else:
        print(f"Error al obtener premios del año {anio}: {response.status_code}")

# Función para obtener premios por categoría
def obtener_premios_por_categoria():
    categoria = input("Ingrese una categoria: ")
    response = requests.get(f"{base_url}/prize/category/{categoria}")
    if response.status_code == 200:
        print(f"Premios en la categoría {categoria}:")
        pprint(response.json())
    else:
        print(f"Error al obtener premios en la categoría {categoria}: {response.status_code}")

# Función para agregar un nuevo premio
def agregar_premio():
    nuevo_premio = {
        "year": int(input("Ingrese el año del premio: ")),
        "category": input("Ingrese la categoría: "),
        "laureates": [
            {
                "id": int(input("Ingrese el ID del laureado: ")),
                "firstname": input("Ingrese el primer nombre: "),
                "surname": input("Ingrese el apellido: "),
                "motivation": input("Ingrese la motivación: "),
                "share": int(input("Ingrese el porcentaje de compartir el premio: "))
            }
        ]
    }
    response = requests.post(f"{base_url}/prizes", json=nuevo_premio)
    if response.status_code == 200:
        print("Premio agregado exitosamente:")
        pprint(response.json())
    else:
        print(f"Error al agregar premio: {response.status_code}")

# Función para actualizar un premio por id de laureado
def actualizar_premio():
    id_laureado = int(input("Ingrese el ID de Laureado para actualizar: "))
    premio_actualizado = {
        "year": int(input("Ingrese el año del premio actualizado: ")),
        "category": input("Ingrese la categoría del premio actualizado: "),
        "laureates": [
            {
                "id": int(input("Ingrese el ID del laureado: ")),
                "firstname": input("Ingrese el primer nombre: "),
                "surname": input("Ingrese el apellido: "),
                "motivation": input("Ingrese la motivación: "),
                "share": int(input("Ingrese el porcentaje de compartir el premio: "))
            }
        ]
    }
    response = requests.put(f"{base_url}/prize/{id_laureado}", json=premio_actualizado)
    if response.status_code == 200:
        print(f"Premio para el laureado con ID {id_laureado} actualizado exitosamente:")
        pprint(response.json())
    else:
        print(f"Error al actualizar el premio: {response.status_code}")

# Función para eliminar un premio por id de laureado
def eliminar_premio():
    id_laureado = int(input("Ingrese el ID de Laureado para eliminar: "))
    response = requests.delete(f"{base_url}/prize/laureate/{id_laureado}")
    if response.status_code == 200:
        print(f"Premio del laureado con ID {id_laureado} eliminado exitosamente.")
    else:
        print(f"Error al eliminar el premio: {response.status_code}")

# Función para mostrar el menú y procesar las opciones
def menu():
    while True:
        print("\nMenú de Opciones:")
        print("1. Obtener todos los premios")
        print("2. Obtener premios por año")
        print("3. Obtener premios por categoría")
        print("4. Agregar un premio")
        print("5. Actualizar un premio")
        print("6. Eliminar un premio")
        print("7. Salir")
        
        try:
            opcion = int(input("Seleccione una opción (1-7): "))
            if opcion == 1:
                obtener_premios()
            elif opcion == 2:
                obtener_premios_por_anio()
            elif opcion == 3:
                obtener_premios_por_categoria()
            elif opcion == 4:
                agregar_premio()
            elif opcion == 5:
                actualizar_premio()
            elif opcion == 6:
                eliminar_premio()
            elif opcion == 7:
                print("Muchas gracias por utilizar la API de los Premios Nobel!")
                break
            else:
                print("Opción no válida, por favor elija entre 1 y 7.")
        except ValueError:
            print("Por favor ingrese un número válido entre 1 y 7.")

# Ejecutar el menú
menu()
