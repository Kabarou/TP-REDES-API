from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import json
from typing import List, Optional
import os
import datetime
from typing import ClassVar

app = FastAPI()

# Definimos el modelo para el laureado
class Laureate(BaseModel):
    id: int
    firstname: str
    surname: Optional[str] = None  # Hacemos 'surname' opcional
    motivation: str
    share: int = Field(ge=1)  # Garantizamos que 'share' sea mayor o igual a 1

# Definimos el modelo para el premio
class Prize(BaseModel):
    year: int
    category: str
    laureates: List[Laureate] = []

# Cargar los datos desde el archivo JSON
def cargar_data():
    directorio_actual = os.path.dirname(__file__)
    ruta_archivo = os.path.join(directorio_actual, 'prizes.json')
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convertir cadenas numéricas a enteros
    for prize in data["prizes"]:
        prize["year"] = int(prize["year"])
        for laureate in prize.get("laureates", []):
            laureate["id"] = int(laureate["id"])
            laureate["share"] = int(laureate["share"])
    
    return data

# Guardar los datos en el archivo JSON
def guardar_data(data):
    directorio_actual = os.path.dirname(__file__)
    ruta_archivo = os.path.join(directorio_actual, 'prizes.json')
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

# Obtener todos los premios
@app.get("/prizes", response_model=List[Prize])
def obtener_premios():
    data = cargar_data()
    return [Prize(**prize) for prize in data['prizes']]

# Obtener premios por año
@app.get("/prize/{year}", response_model=List[Prize])
def obtener_premios_por_anio(anio: int):
    data = cargar_data()
    prizes = [prize for prize in data['prizes'] if prize['year'] == anio]
    if not prizes:
        raise HTTPException(status_code=404, detail="No se encontraron premios para este año")
    return prizes

@app.get("/prize/category/{category}", response_model=List[Prize])
def obtener_premios_por_categoria(category: str):
    data = cargar_data()
    prizes = [prize for prize in data['prizes'] if prize['category'] == category]
    if not prizes:
        raise HTTPException(status_code=404, detail="No se encontraron premios para esta categoría")
    return prizes

# Agregar un nuevo premio
@app.post("/prizes", response_model=Prize)
def agregar_premio(prize: Prize):
    data = cargar_data()
    new_prize = prize.model_dump()  # Usamos model_dump()
    data['prizes'].append(new_prize)
    guardar_data(data)
    return new_prize

# Actualizar un premio por id de laureado
@app.put("/prize/{laureate_id}", response_model=Prize)
def actualizar_premio(laureate_id: int, prize: Prize):
    data = cargar_data()
    prize_found = False
    
    # Buscar el premio con el laureado específico
    for p in data['prizes']:
        # Verificar si la clave 'laureates' existe antes de acceder
        if 'laureates' in p:
            for laureate in p['laureates']:
                if laureate['id'] == laureate_id:  # Buscar por ID del laureado
                    # Actualizar solo el laureado específico sin anidar laureados
                    laureate['firstname'] = prize.laureates[0].firstname
                    laureate['surname'] = prize.laureates[0].surname
                    laureate['motivation'] = prize.laureates[0].motivation
                    laureate['share'] = prize.laureates[0].share
                    prize_found = True
                    break
        if prize_found:
            break
    
    if not prize_found:
        raise HTTPException(status_code=404, detail="Premio no encontrado para este laureado")
    
    guardar_data(data)
    return prize


# Eliminar un premio por el ID del laureado
@app.delete("/prize/laureate/{laureate_id}")
def borrar_premio_por_laureate(laureate_id: int):
    data = cargar_data()
    
    # Buscar y eliminar el laureado dentro de los premios
    prize_found = False
    
    for prize in data['prizes']:
        # Verificar si el premio tiene laureados
        if 'laureates' in prize and prize['laureates']:
            laureates = prize['laureates']
            # Filtrar los laureates que no coinciden con el id
            new_laureates = [laureate for laureate in laureates if laureate['id'] != laureate_id]
            
            # Si el laureado fue encontrado y eliminado, actualizamos la lista
            if len(new_laureates) != len(laureates):
                prize['laureates'] = new_laureates
                prize_found = True
                
                # Si el premio no tiene laureados después de eliminar, eliminamos el premio
                if not prize['laureates']:
                    data['prizes'].remove(prize)
                break
    
    if not prize_found:
        raise HTTPException(status_code=404, detail="No se encontró el laureado con ese ID en los premios")
    
    # Guardar los datos después de la eliminación
    guardar_data(data)
    return {"Mensaje": f"Premio del laureado con ID {laureate_id} eliminado correctamente."}
