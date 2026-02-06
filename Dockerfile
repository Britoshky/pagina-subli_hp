# Imagen base de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorio para sesiones de Flask
RUN mkdir -p flask_session

# Exponer el puerto (se usa variable de entorno PORT)
EXPOSE ${PORT:-2000}

# Comando de inicio con gunicorn
CMD gunicorn --bind 0.0.0.0:${PORT:-2000} --workers 4 --timeout 120 --access-logfile - --error-logfile - app:app
