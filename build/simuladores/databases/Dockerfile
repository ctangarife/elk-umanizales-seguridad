FROM python:3.11-slim

# Instalar dependencias y herramientas necesarias
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    vim \
    htop \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Instalar librerías Python necesarias
RUN pip install --no-cache-dir \
    requests \
    faker \
    python-dateutil \
    colorama \
    mysql-connector-python \
    psycopg2-binary

# Crear directorio de trabajo
WORKDIR /app

# Crear directorio para logs
RUN mkdir -p /app/logs

# Configurar variables de entorno por defecto
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO
