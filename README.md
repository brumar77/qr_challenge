# QR Code Scanner App

Esta es una aplicación para escanear códigos QR, construida con FastAPI. La app está configurada para ejecutarse en un entorno Docker.

## Requisitos

Antes de comenzar, asegúrate de tener instalados los siguientes programas:

- [Docker](https://www.docker.com/) (incluye Docker Compose)
- [Python](https://www.python.org/)
  
## Instrucciones para ejecutar la aplicación

1. Crea un entorno virtual en Python, desde la raiz del proyecto:

   ```bash
   python3 -m venv venv
   ```
   a. Activa el entorno virtual:

      ```bash
      source venv/bin/activate
      ```
    b. Instala las dependencias:

      ```bash
      pip install -r requirements.txt
      ```

2. Levanta el entorno Docker con Docker Compose, desde la raiz del proyecto:

   ```bash
   docker compose up -d --build
   ```
3. Ubicate en el path correcto.
Levanta el servicio FastAPI con:

   ```bash
   uvicorn main:app --reload
   ```

3. Accede a la app en [http://localhost:8000/docs](http://localhost:8000/docs)


## Instrucciones para ejecutar los test de pytest
1. Desde la raiz, ejecutar por consola:

   ```bash
   pytest
   ```
   o si necesitas mas detalles:

   ```bash
   pytest -v
   ```

