# Usa una imagen oficial de Python ligera
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala las dependencias del sistema necesarias para compilar ciertos paquetes
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos de requerimientos primero (para aprovechar el caché de Docker)
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código del backend al contenedor
COPY . .

# Exponer el puerto (Render inyecta la variable de entorno $PORT dinámicamente)
EXPOSE 8000

# Comando para ejecutar la aplicación con Uvicorn
# Se usa $PORT por defecto (Render lo asigna, usualmente el 10000) o 8000 como fallback
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
