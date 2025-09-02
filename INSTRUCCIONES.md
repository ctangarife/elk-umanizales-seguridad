# 📋 Instrucciones Básicas - Stack ELK

## ⚡ Pasos para Empezar

### 1️⃣ Crear archivo de configuración
```bash
# Opción 1: Copiar desde el ejemplo
cp env.example .env

# Opción 2: Crear manualmente
echo "ELASTIC_PASSWORD=elastic123" > .env
```

### 2️⃣ Levantar servicios
```bash
# Primera vez o después de cambios en Dockerfiles
docker compose up -d --build

# Para ejecuciones posteriores
docker compose up -d
```

### 3️⃣ Abrir Kibana
- URL: http://localhost:5601
- Usuario: `elastic`
- Contraseña: `elastic123`

### 4️⃣ Configurar Templates de Índice (Opcional)
```powershell
# Configurar templates usando PowerShell
Invoke-RestMethod -Uri "http://localhost:9200/_template/web-logs-template" -Method PUT -ContentType "application/json" -Body '{"index_patterns": ["web-logs-*"], "settings": {"number_of_shards": 3, "number_of_replicas": 1, "refresh_interval": "1s"}, "mappings": {"properties": {"@timestamp": {"type": "date"}, "clientip": {"type": "ip"}, "method": {"type": "keyword"}, "request": {"type": "text"}, "response": {"type": "integer"}, "bytes": {"type": "long"}, "referrer": {"type": "text"}, "agent": {"type": "text"}}}}'

Invoke-RestMethod -Uri "http://localhost:9200/_template/db-logs-template" -Method PUT -ContentType "application/json" -Body '{"index_patterns": ["db-logs-*"], "settings": {"number_of_shards": 3, "number_of_replicas": 1, "refresh_interval": "1s"}, "mappings": {"properties": {"@timestamp": {"type": "date"}, "db_type": {"type": "keyword"}, "db_user": {"type": "keyword"}, "db_name": {"type": "keyword"}, "query_time": {"type": "float"}, "rows_sent": {"type": "integer"}, "rows_examined": {"type": "integer"}}}}'

Invoke-RestMethod -Uri "http://localhost:9200/_template/micro-logs-template" -Method PUT -ContentType "application/json" -Body '{"index_patterns": ["micro-logs-*"], "settings": {"number_of_shards": 3, "number_of_replicas": 1, "refresh_interval": "1s"}, "mappings": {"properties": {"@timestamp": {"type": "date"}, "level": {"type": "keyword"}, "service": {"type": "keyword"}, "message": {"type": "text"}, "trace_id": {"type": "keyword"}, "user_id": {"type": "keyword"}, "duration_ms": {"type": "integer"}, "http_status": {"type": "integer"}}}}'
```

### 5️⃣ Crear Index Patterns
1. Ve a "Stack Management" → "Index Patterns"
2. Crea estos patrones:
   - `web-logs-*`
   - `db-logs-*`
   - `micro-logs-*`

### 5️⃣ Ver datos
1. Ve a "Analytics" → "Discover"
2. Selecciona un index pattern
3. ¡Verás logs en tiempo real!

## 🎮 Comandos Útiles

```bash
# Ver estado de servicios
docker compose ps

# Ver logs en tiempo real
docker compose logs -f

# Detener servicios
docker compose down

# Reiniciar servicios
docker compose restart
```

## 🆘 ¿Problemas?

- **Kibana no carga**: Espera 2-3 minutos
- **No veo datos**: Verifica que los simuladores estén corriendo
- **Errores**: Revisa los logs con `docker compose logs`

---
**¡Listo! Ya tienes ELK funcionando 🎉**
