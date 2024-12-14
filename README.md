Este proyecto es una API creada con **FastAPI**, que permite gestionar premios y laureados.
Las instrucciones son las siguientes:

## Requisitos

- **Python 3.13.0** o superior instalado en tu sistema.
- Conexión a internet para instalar dependencias.


## Comandos

Ejecutar el siguiente comando en WINDOWS:

python -m venv .venv #para crear un entorno virtual
.venv\Scripts\activate.bat   #para activarlo


Una vez hecho esto, debes descargar las librerias necesarias:

pip install -r requirements.txt 


Luego debemos levantar el servidor:

uvicorn servidor_api:app --host 0.0.0.0 --port 8000


Interfaz grafica de la API:

http://127.0.0.1:8000/docs