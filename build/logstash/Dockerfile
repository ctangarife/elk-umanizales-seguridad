FROM logstash:8.11.0

# Instalar dependencias y herramientas necesarias
USER root

# Instalar herramientas de monitoreo y debugging
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    vim \
    htop \
    net-tools \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Instalar plugins adicionales de Logstash
RUN /usr/share/logstash/bin/logstash-plugin install logstash-input-beats
RUN /usr/share/logstash/bin/logstash-plugin install logstash-input-tcp
RUN /usr/share/logstash/bin/logstash-plugin install logstash-input-http
RUN /usr/share/logstash/bin/logstash-plugin install logstash-filter-mutate
RUN /usr/share/logstash/bin/logstash-plugin install logstash-filter-grok
RUN /usr/share/logstash/bin/logstash-plugin install logstash-filter-date
RUN /usr/share/logstash/bin/logstash-plugin install logstash-output-elasticsearch

# Crear directorios para configuraciones personalizadas
RUN mkdir -p /usr/share/logstash/pipeline/custom
RUN mkdir -p /usr/share/logstash/config/custom

# Configurar permisos
RUN chown -R logstash:logstash /usr/share/logstash/pipeline/custom
RUN chown -R logstash:logstash /usr/share/logstash/config/custom

# Volver al usuario logstash
USER logstash
