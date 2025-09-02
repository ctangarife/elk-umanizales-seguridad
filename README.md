# 🚀 Stack ELK con Docker Compose - Guía Completa para Principiantes

**¡Aprende ELK de forma práctica y comprensible!** Este proyecto te permite experimentar con Elasticsearch, Logstash y Kibana usando Docker Compose, con explicaciones paso a paso para desarrolladores junior y estudiantes universitarios.

## 🎯 ¿Qué es ELK y por qué es importante?

### **¿Qué significa ELK?**
ELK es un acrónimo que representa tres herramientas que trabajan juntas para analizar logs (registros) de aplicaciones:

- **E**lasticsearch: Es como una "biblioteca gigante" que almacena y organiza todos los logs
- **L**ogstash: Es como un "filtro inteligente" que limpia y organiza los logs antes de guardarlos
- **K**ibana: Es como un "tablero de control" que te permite ver y analizar los logs de forma visual

### **¿Por qué necesitas ELK?**
Imagina que tienes 100 servidores web funcionando. Cada uno genera miles de logs por día. Sin ELK:
- ❌ Sería imposible revisar todos los logs manualmente
- ❌ No podrías encontrar errores rápidamente
- ❌ No tendrías alertas cuando algo falla
- ❌ No podrías ver patrones o tendencias

**Con ELK puedes:**
- ✅ Buscar en millones de logs en segundos
- ✅ Crear alertas automáticas cuando algo falla
- ✅ Ver gráficos y estadísticas en tiempo real
- ✅ Detectar problemas antes de que afecten a los usuarios

## 🏗️ Arquitectura del Sistema - Explicación Simple

### **¿Cómo funciona todo junto?**

```
📱 Usuarios → 🌐 Servidores Web → 📝 Logs → 🔄 Logstash → 🗄️ Elasticsearch → 📊 Kibana
```

**Paso a paso:**
1. **Usuarios** visitan tu sitio web
2. **Servidores web** registran cada visita en archivos de log
3. **Logstash** lee esos logs, los limpia y los organiza
4. **Elasticsearch** almacena los logs organizados para búsquedas rápidas
5. **Kibana** te muestra gráficos y estadísticas de esos logs

### **¿Por qué 3 nodos de Elasticsearch?**
- **Nodo 1**: Si falla, los otros dos siguen funcionando
- **Nodo 2**: Si falla, los otros dos siguen funcionando  
- **Nodo 3**: Si falla, los otros dos siguen funcionando

Es como tener **3 copias de seguridad** de tu información. Si uno se rompe, los otros siguen funcionando.

## 📊 Datos Simulados - ¿Qué significa cada cosa?

### **¿Por qué simulamos datos?**
En el mundo real, los logs vienen de aplicaciones reales. Pero para aprender, necesitamos datos que podamos controlar y entender.

### **50 Servidores Web** 🌐
- **¿Qué son?**: Simulan servidores como Apache o Nginx que sirven páginas web
- **¿Qué generan?**: Logs como "Usuario X visitó la página Y a las 15:30"
- **Ejemplo real**: `192.168.1.100 - - [01/Sep/2025:15:30:45] "GET /api/users HTTP/1.1" 200 1234`
- **¿Por qué 50?**: Para simular una empresa real que tiene muchos servidores

### **5 Bases de Datos** 🗄️
- **¿Qué son?**: Simulan bases de datos como MySQL o PostgreSQL
- **¿Qué generan?**: Logs de consultas como "Usuario X buscó información Y"
- **Ejemplo real**: `{"timestamp": "2025-09-01T15:30:45", "query": "SELECT * FROM users", "duration_ms": 45}`
- **¿Por qué 5?**: Para simular diferentes tipos de bases de datos (usuarios, productos, ventas, etc.)

### **10 Microservicios** 🔧
- **¿Qué son?**: Simulan pequeñas aplicaciones que hacen una cosa específica
- **¿Qué generan?**: Logs estructurados como "El servicio de autenticación procesó un login"
- **Ejemplo real**: `{"service": "auth-service", "message": "User login successful", "user_id": "12345"}`
- **¿Por qué 10?**: Para simular una arquitectura moderna de microservicios

## 🚀 Inicio Rápido - Paso a Paso para Principiantes

### **¿Qué necesitas antes de empezar?**
- **Docker Desktop** instalado en tu computadora
- **Git** para descargar el proyecto
- **Un editor de código** (VS Code, Sublime Text, etc.)
- **Al menos 16GB de RAM** (24GB recomendado)

### **1️⃣ Descargar el proyecto**
```bash
# Descargar el proyecto desde GitHub
git clone https://github.com/tu-usuario/elk-stack.git

# Entrar al directorio del proyecto
cd elk-stack
```

### **2️⃣ Crear archivo de configuración**
```bash
# Opción 1: Copiar desde el ejemplo (recomendado)
cp env.example .env

# Opción 2: Crear manualmente
# Windows (PowerShell)
echo "ELASTIC_PASSWORD=elastic123" > .env

# Linux/Mac
echo "ELASTIC_PASSWORD=elastic123" > .env
```

**¿Qué hace este archivo?**
El archivo `.env` contiene variables de configuración como contraseñas. Es como un "archivo de secretos" que Docker usa para configurar los servicios.

### **3️⃣ Levantar servicios**
```bash
# Primera vez o después de cambios en Dockerfiles
docker compose up -d --build

# Para ejecuciones posteriores
docker compose up -d
```

**¿Qué hace este comando?**
- `docker compose up`: Levanta todos los servicios definidos en el archivo docker-compose.yml
- `-d`: Ejecuta en segundo plano (detached mode)
- `--build`: Construye las imágenes Docker si han cambiado

**¿Cuánto tiempo tarda?**
- Primera vez: 5-10 minutos (descarga imágenes y construye contenedores)
- Veces posteriores: 2-3 minutos (solo levanta contenedores existentes)

### **4️⃣ Verificar que todo funcione**
```bash
# Ver el estado de todos los servicios
docker compose ps

# Ver logs en tiempo real
docker compose logs -f
```

**¿Qué deberías ver?**
- Todos los servicios en estado "Up" y "healthy"
- Logs mostrando que los servicios se están iniciando correctamente

### **5️⃣ Abrir Kibana**
- **URL**: http://localhost:5601
- **Usuario**: `elastic`
- **Contraseña**: `elastic123`

**¿Qué es Kibana?**
Kibana es la interfaz web que te permite ver y analizar los logs. Es como "la cara bonita" de todo el sistema.

## 🎮 Comandos Básicos - Tu Kit de Herramientas

### **Comandos para el día a día**

```bash
# Iniciar servicios
docker compose up -d

# Ver logs en tiempo real (útil para debugging)
docker compose logs -f

# Ver estado de servicios
docker compose ps

# Detener servicios
docker compose down

# Reiniciar servicios
docker compose restart

# Ver logs de un servicio específico
docker compose logs elasticsearch-1

# Ver estadísticas de recursos (CPU, memoria)
docker stats
```

### **¿Cuándo usar cada comando?**

- **`docker compose up -d`**: Cuando quieras iniciar todo el sistema
- **`docker compose logs -f`**: Cuando algo no funcione y quieras ver qué está pasando
- **`docker compose ps`**: Para verificar que todos los servicios estén funcionando
- **`docker compose down`**: Cuando quieras detener todo y liberar recursos
- **`docker stats`**: Para ver si algún servicio está consumiendo demasiados recursos

## 📈 Primeros Pasos en Kibana - Tu Primer Dashboard

### **¿Qué es Kibana?**
Kibana es como un "Excel visual" para logs. Te permite crear gráficos, tablas y dashboards con los datos de Elasticsearch.

### **1️⃣ Abrir Kibana**
- Ve a http://localhost:5601
- Inicia sesión con `elastic` / `elastic123`

### **2️⃣ Crear Index Patterns**
Los "Index Patterns" le dicen a Kibana dónde buscar los datos.

**Paso a paso:**
1. Ve a **"Stack Management"** (ícono de engranaje)
2. Haz clic en **"Index Patterns"**
3. Haz clic en **"Create index pattern"**
4. Crea estos tres patrones:
   - `web-logs-*` (para logs de servidores web)
   - `db-logs-*` (para logs de bases de datos)
   - `micro-logs-*` (para logs de microservicios)

**¿Qué significa el asterisco (*)?**
El asterisco significa "cualquier cosa". `web-logs-*` incluirá:
- `web-logs-2025.09.01`
- `web-logs-2025.09.02`
- `web-logs-2025.09.03`
- etc.

### **3️⃣ Ver datos en Discover**
"Discover" es como una "lupa gigante" para explorar tus datos.

**Paso a paso:**
1. Ve a **"Analytics"** → **"Discover"**
2. Selecciona un index pattern (por ejemplo, `web-logs-*`)
3. Haz clic en **"Refresh"**
4. ¡Verás logs en tiempo real!

**¿Qué verás?**
- Una tabla con todos los logs
- Campos como timestamp, IP del cliente, método HTTP, etc.
- Filtros para buscar logs específicos

### **4️⃣ Crear tu primer gráfico**
**Paso a paso:**
1. Ve a **"Analytics"** → **"Visualize Library"**
2. Haz clic en **"Create visualization"**
3. Selecciona **"Line"** (gráfico de líneas)
4. Selecciona tu index pattern
5. En el eje X, selecciona `@timestamp`
6. En el eje Y, selecciona `Count`
7. Haz clic en **"Save"**

**¿Qué has creado?**
Un gráfico que muestra cuántos logs se generan a lo largo del tiempo. Es útil para ver patrones como "picos de tráfico" o "horas de menor actividad".

## 🏗️ Arquitectura Detallada - Entendiendo Cada Pieza

### **¿Por qué Docker Compose?**
Docker Compose es como un "director de orquesta" que coordina todos los servicios. En lugar de ejecutar 10 comandos separados, ejecutas uno solo y todo se configura automáticamente.

### **¿Qué hace cada servicio?**

#### **Elasticsearch (3 nodos)**
- **¿Qué es?**: Una base de datos especializada en búsquedas rápidas
- **¿Por qué 3 nodos?**: Para alta disponibilidad (si uno falla, los otros siguen funcionando)
- **¿Qué almacena?**: Todos los logs procesados por Logstash
- **¿Por qué es rápido?**: Usa índices especiales y caché en memoria

#### **Logstash**
- **¿Qué es?**: Un procesador de logs que limpia y organiza la información
- **¿Qué hace?**: Lee logs de diferentes fuentes, los limpia y los envía a Elasticsearch
- **¿Por qué es importante?**: Sin Logstash, tendrías logs en diferentes formatos y sería imposible analizarlos

#### **Kibana**
- **¿Qué es?**: La interfaz web para visualizar y analizar datos
- **¿Qué hace?**: Te permite crear gráficos, tablas y dashboards
- **¿Por qué es útil?**: Convierte datos complejos en información visual fácil de entender

#### **Simuladores**
- **¿Qué son?**: Programas que generan logs de prueba
- **¿Por qué los necesitamos?**: Para tener datos realistas sin afectar sistemas reales
- **¿Cómo funcionan?**: Generan logs cada 5-10 segundos y los envían a Logstash

#### **Monitor (elk-monitor)**
- **¿Qué es?**: Un programa que verifica que todos los servicios estén funcionando
- **¿Qué hace?**: Cada 5 minutos verifica Elasticsearch, Logstash y Kibana
- **¿Por qué es útil?**: Te avisa si algo falla antes de que te des cuenta

## 📁 Estructura del Proyecto - ¿Dónde está cada cosa?

```
proyecto/
├── build/                          # Dockerfiles (instrucciones para construir contenedores)
│   ├── elasticsearch/              # Cómo construir el contenedor de Elasticsearch
│   ├── logstash/                   # Cómo construir el contenedor de Logstash
│   ├── kibana/                     # Cómo construir el contenedor de Kibana
│   └── simuladores/                # Cómo construir los simuladores
├── data/                           # Datos y configuraciones
│   ├── elasticsearch/              # Configuración de Elasticsearch
│   ├── logstash/                   # Configuración de Logstash
│   ├── kibana/                     # Configuración de Kibana
│   └── simuladores/                # Scripts de los simuladores
├── bd/                             # Datos persistentes (bases de datos)
├── docker-compose.yml              # Archivo principal que coordina todo
└── README.md                       # Este archivo
```

### **¿Qué es cada carpeta?**

- **`build/`**: Contiene instrucciones para construir contenedores personalizados
- **`data/`**: Contiene configuraciones y scripts que se copian a los contenedores
- **`bd/`**: Contiene datos que persisten entre reinicios (como bases de datos)
- **`docker-compose.yml`**: El archivo principal que define todos los servicios

## 🔧 Configuración Avanzada - Personalizando tu Stack

### **¿Cómo cambiar la configuración?**

#### **Cambiar puertos**
Si quieres usar puertos diferentes (por ejemplo, si el 5601 ya está ocupado):

```yaml
# En docker-compose.yml
kibana:
  ports:
    - "8080:5601"  # Ahora Kibana estará en http://localhost:8080
```

#### **Cambiar memoria**
Si quieres dar más memoria a Elasticsearch:

```yaml
# En docker-compose.yml
elasticsearch-1:
  environment:
    - "ES_JAVA_OPTS=-Xms2g -Xmx2g"  # 2GB en lugar de 1GB
```

#### **Agregar más simuladores**
Si quieres simular más servidores:

```yaml
# En docker-compose.yml
web-simulator:
  environment:
    - NUM_SERVERS=100  # 100 servidores en lugar de 50
```

### **¿Qué archivos puedes modificar?**

- **`docker-compose.yml`**: Para cambiar puertos, memoria, volúmenes
- **`data/logstash/pipeline/logstash.conf`**: Para cambiar cómo se procesan los logs
- **`data/simuladores/*/generate_*.py`**: Para cambiar qué tipos de logs se generan

## 🚨 Solución de Problemas Comunes

### **Problema: Los servicios no inician**
```bash
# Ver logs de error
docker compose logs

# Verificar recursos del sistema
docker stats

# Reiniciar todo
docker compose down
docker compose up -d
```

### **Problema: Kibana no se abre**
```bash
# Verificar que Kibana esté funcionando
docker compose ps kibana

# Ver logs de Kibana
docker compose logs kibana

# Verificar que Elasticsearch esté funcionando
curl http://localhost:9200
```

### **Problema: Los simuladores no generan logs**
```bash
# Verificar que los simuladores estén funcionando
docker compose ps | grep simulator

# Ver logs de un simulador específico
docker compose logs web-simulator

# Reiniciar simuladores
docker compose restart web-simulator db-simulator micro-simulator
```

### **Problema: Consumo alto de CPU/Memoria**
```bash
# Ver uso de recursos
docker stats

# Si Elasticsearch consume mucho CPU
docker compose restart elasticsearch-1 elasticsearch-2 elasticsearch-3

# Si Logstash consume mucha memoria
docker compose restart logstash
```

## 📚 Conceptos Clave para Entender

### **¿Qué es un log?**
Un log es un registro de algo que pasó en tu sistema. Por ejemplo:
- "Usuario X se conectó a las 15:30"
- "Error 404 en la página /admin"
- "Base de datos respondió en 45ms"

### **¿Qué es un índice?**
Un índice es como una "carpeta" en Elasticsearch donde se guardan logs relacionados. Por ejemplo:
- `web-logs-2025.09.01`: Logs de servidores web del 1 de septiembre
- `db-logs-2025.09.01`: Logs de bases de datos del 1 de septiembre

### **¿Qué es un pipeline?**
Un pipeline es una serie de pasos que Logstash sigue para procesar logs:
1. **Input**: Leer logs de una fuente
2. **Filter**: Limpiar y organizar los logs
3. **Output**: Enviar logs procesados a Elasticsearch

### **¿Qué es un dashboard?**
Un dashboard es una página en Kibana que muestra múltiples gráficos y tablas relacionados. Es como un "tablero de control" que te da una vista completa de tu sistema.

## 🎯 Próximos Pasos - ¿Qué aprender después?

### **1. Crear dashboards personalizados**
- Gráficos de errores por hora
- Tablas de usuarios más activos
- Alertas cuando algo falla

### **2. Configurar alertas**
- Email cuando hay muchos errores 500
- Notificación cuando un servicio está caído
- Alerta cuando el tráfico es muy alto

### **3. Integrar con aplicaciones reales**
- Conectar tu aplicación web real
- Conectar tu base de datos real
- Conectar tus microservicios reales

### **4. Aprender más sobre Elasticsearch**
- Queries avanzadas
- Agregaciones (group by, count, sum)
- Mapeo de campos personalizado

## 🤝 Contribuir y Obtener Ayuda

### **¿Encontraste un bug?**
1. Revisa si ya está reportado en GitHub
2. Crea un nuevo issue con detalles del problema
3. Incluye logs de error y pasos para reproducir

### **¿Quieres mejorar algo?**
1. Haz un fork del proyecto
2. Crea una rama para tu mejora
3. Haz commit y push de tus cambios
4. Crea un pull request

### **¿Tienes preguntas?**
1. Revisa la documentación oficial de ELK
2. Busca en Stack Overflow
3. Pregunta en foros de la comunidad

## 📖 Recursos Adicionales

### **Documentación Oficial**
- [Elasticsearch Guide](https://www.elastic.co/guide/index.html)
- [Logstash Reference](https://www.elastic.co/guide/en/logstash/current/index.html)
- [Kibana User Guide](https://www.elastic.co/guide/en/kibana/current/index.html)

### **Tutoriales y Cursos**
- [Elasticsearch: The Definitive Guide](https://www.elastic.co/guide/en/elasticsearch/guide/current/index.html)
- [Logstash Tutorial](https://www.elastic.co/guide/en/logstash/current/getting-started-with-logstash.html)
- [Kibana Tutorial](https://www.elastic.co/guide/en/kibana/current/getting-started.html)

### **Comunidad**
- [Elastic Forums](https://discuss.elastic.co/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/elasticsearch)
- [Reddit r/elasticsearch](https://www.reddit.com/r/elasticsearch/)

## 🎉 ¡Felicidades!

Si llegaste hasta aquí, ya tienes una comprensión sólida del stack ELK y cómo usarlo. Recuerda:

- **La práctica hace al maestro**: Experimenta con diferentes configuraciones
- **No tengas miedo de romper algo**: Puedes reiniciar todo fácilmente
- **Pregunta cuando tengas dudas**: La comunidad de ELK es muy amigable
- **Comparte lo que aprendes**: Ayuda a otros desarrolladores

¡Ahora ve y crea algo increíble con ELK! 🚀

---

**¿Te gustó este proyecto?** ⭐ Dale una estrella en GitHub y compártelo con otros desarrolladores que quieran aprender ELK.

