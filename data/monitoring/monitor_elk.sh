#!/bin/bash

echo "Iniciando monitoreo del stack ELK..."
echo "Fecha de inicio: $(date)"
echo "================================="

while true; do
  echo ""
  echo "=== Estado del Stack ELK - $(date) ==="
  
  # Verificar Elasticsearch Cluster
  echo "🔍 Elasticsearch Cluster:"
  if response=$(curl -s http://elk-elasticsearch:9200/_cluster/health 2>/dev/null); then
    if echo "$response" | grep -q "status"; then
      status=$(echo "$response" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
      nodes=$(echo "$response" | grep -o '"number_of_nodes":[0-9]*' | cut -d':' -f2)
      echo "✅ Elasticsearch: OK - Status: $status, Nodos: $nodes"
    else
      echo "⚠️  Elasticsearch: Respuesta inesperada"
    fi
  else
    echo "❌ Elasticsearch: ERROR - No se puede conectar"
  fi
  
  # Verificar Logstash
  echo "🔍 Logstash Status:"
  if response=$(curl -s http://elk-logstash:9600/_node/stats 2>/dev/null); then
    if echo "$response" | grep -q "jvm"; then
      echo "✅ Logstash: OK - API respondiendo"
    else
      echo "⚠️  Logstash: Respuesta inesperada"
    fi
  else
    echo "❌ Logstash: ERROR - No se puede conectar"
  fi
  
  # Verificar Kibana
  echo "🔍 Kibana Status:"
  if response=$(curl -s http://elk-kibana:5601/api/status 2>/dev/null); then
    if echo "$response" | grep -q "status"; then
      echo "✅ Kibana: OK - API respondiendo"
    else
      echo "⚠️  Kibana: Respuesta inesperada"
    fi
  else
    echo "❌ Kibana: ERROR - No se puede conectar"
  fi
  
  # Verificar simuladores
  echo "🔍 Simuladores:"
  if docker ps | grep -q "web-simulator"; then
    echo "✅ Web Simulator: Activo"
  else
    echo "❌ Web Simulator: Inactivo"
  fi
  
  if docker ps | grep -q "db-simulator"; then
    echo "✅ DB Simulator: Activo"
  else
    echo "❌ DB Simulator: Inactivo"
  fi
  
  if docker ps | grep -q "micro-simulator"; then
    echo "✅ Micro Simulator: Activo"
  else
    echo "❌ Micro Simulator: Inactivo"
  fi
  
  echo "================================="
  echo "⏰ Próxima verificación en 5 minutos..."
  echo "================================="
  sleep 300
done
