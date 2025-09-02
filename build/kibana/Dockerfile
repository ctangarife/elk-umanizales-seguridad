FROM kibana:8.11.0

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

# Crear directorios para dashboards y configuraciones personalizadas
RUN mkdir -p /usr/share/kibana/dashboards/custom
RUN mkdir -p /usr/share/kibana/config/custom

# Configurar permisos
RUN chown -R kibana:kibana /usr/share/kibana/dashboards/custom
RUN chown -R kibana:kibana /usr/share/kibana/config/custom

# Volver al usuario kibana
USER kibana
