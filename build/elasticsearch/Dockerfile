FROM elasticsearch:8.11.0

# Instalar dependencias y herramientas necesarias
USER root

# Instalar herramientas de monitoreo y debugging
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    vim \
    htop \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# No crear plugins personalizados - usar configuración estándar

# Volver al usuario elasticsearch
USER elasticsearch
