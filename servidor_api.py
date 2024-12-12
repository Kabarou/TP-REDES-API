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

# Agregar un nuevo premio
@app.post("/prizes", response_model=Prize)
def agregar_premio(prize: Prize):
    data = cargar_data()
    new_prize = prize.model_dump()  # Usamos model_dump()
    data['prizes'].append(new_prize)
    guardar_data(data)
    return new_prize

# Actualizar un premio por año
@app.put("/prize/{year}", response_model=Prize)
def actualizar_premio(anio: int, prize: Prize):
    data = cargar_data()
    prize_found = False
    for p in data['prizes']:
        if p['year'] == anio:
            p.update(prize.model_dump())  # Usamos model_dump()
            prize_found = True
            break
    if not prize_found:
        raise HTTPException(status_code=404, detail="Premio no encontrado")
    guardar_data(data)
    return prize

# Actualizar todos los premios de una categoría específica
@app.put("/prize/category/{category}", response_model=List[Prize])
def actualizar_premios_por_categoria(category: str, prize: Prize):
    data = cargar_data()
    updated_prizes = []
    prize_found = False
    
    # Buscar y actualizar todos los premios de la categoría
    for p in data['prizes']:
        if p['category'] == category:
            p.update(prize.model_dump())  # Usamos model_dump()
            updated_prizes.append(p)
            prize_found = True
    
    if not prize_found:
        raise HTTPException(status_code=404, detail="No se encontraron premios para esta categoría")
    
    guardar_data(data)
    return updated_prizes

# Eliminar un premio por año
@app.delete("/prize/{year}")
def borrar_premio(anio: int):
    data = cargar_data()
    data['prizes'] = [prize for prize in data['prizes'] if prize['year'] != anio]
    guardar_data(data)
    return {"Mensaje": f"Premio del año {anio} eliminado correctamente."}
