#!/bin/bash

echo "Configurando templates de índice para ELK..."

# Esperar a que Elasticsearch esté listo
until curl -s http://localhost:9200/_cluster/health | grep -q "green\|yellow"; do
    echo "Esperando a que Elasticsearch esté listo..."
    sleep 5
done

# Crear template para logs web
curl -X PUT "http://localhost:9200/_template/web-logs-template" -H "Content-Type: application/json" -d '{
  "index_patterns": ["web-logs-*"],
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "refresh_interval": "1s"
  },
  "mappings": {
    "properties": {
      "@timestamp": { "type": "date" },
      "clientip": { "type": "ip" },
      "method": { "type": "keyword" },
      "request": { "type": "text" },
      "response": { "type": "integer" },
      "bytes": { "type": "long" },
      "referrer": { "type": "text" },
      "agent": { "type": "text" }
    }
  }
}'

# Crear template para logs de base de datos
curl -X PUT "http://localhost:9200/_template/db-logs-template" -H "Content-Type: application/json" -d '{
  "index_patterns": ["db-logs-*"],
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "refresh_interval": "1s"
  },
  "mappings": {
    "properties": {
      "@timestamp": { "type": "date" },
      "db_type": { "type": "keyword" },
      "db_user": { "type": "keyword" },
      "db_name": { "type": "keyword" },
      "query_time": { "type": "float" },
      "rows_sent": { "type": "integer" },
      "rows_examined": { "type": "integer" }
    }
  }
}'

# Crear template para logs de microservicios
curl -X PUT "http://localhost:9200/_template/micro-logs-template" -H "Content-Type: application/json" -d '{
  "index_patterns": ["micro-logs-*"],
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "refresh_interval": "1s"
  },
  "mappings": {
    "properties": {
      "@timestamp": { "type": "date" },
      "level": { "type": "keyword" },
      "service": { "type": "keyword" },
      "message": { "type": "text" },
      "trace_id": { "type": "keyword" },
      "user_id": { "type": "keyword" },
      "duration_ms": { "type": "integer" },
      "http_status": { "type": "integer" }
    }
  }
}'

echo "Templates de índice configurados exitosamente!"
