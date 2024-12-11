from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from typing import List, Optional

app = FastAPI()

# Definimos el modelo para el premio
class Laureate(BaseModel):
    id: int
    firstname: str
    surname: str

class Prize(BaseModel):
    year: int
    category: str
    laureates: List[Laureate]

# Cargar los datos desde el archivo JSON
def cargar_data():
    with open('app/prizes.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Guardar los datos en el archivo JSON
def guardar_data(data):
    with open('app/prizes.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

# Obtener todos los premios
@app.get("/prizes", response_model=List[Prize])
def obtener_premios():
    data = cargar_data()
    return data['prizes']

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
    new_prize = prize.dict()
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
            p.update(prize.dict())
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
            p.update(prize.dict())
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
