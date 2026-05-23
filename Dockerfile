# ETAPA 1: Construir el Frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
# Copiar package.json y package-lock.json
COPY frontend/package*.json ./
RUN npm install
# Copiar el resto del código del frontend
COPY frontend/ ./
# Construir la aplicación para producción (se generará la carpeta dist)
RUN npm run build

# ETAPA 2: Construir el Backend y empaquetar todo
FROM python:3.10-slim
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar ciertos paquetes
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requerimientos primero (para aprovechar el caché de Docker)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del backend
COPY backend/ ./

# Copiar el build del frontend a la carpeta static del backend
COPY --from=frontend-builder /app/frontend/dist ./static

# Exponer el puerto (Render inyecta la variable de entorno $PORT dinámicamente)
EXPOSE 8000

# Comando para ejecutar la aplicación con Uvicorn
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
