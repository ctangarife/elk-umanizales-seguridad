# 📊 Dimensionamiento y Cálculo de Capacidades - PoC ELK Stack

## 📋 Resumen Ejecutivo

Este documento presenta el dimensionamiento completo del sistema centralizador de logs ELK (Elasticsearch, Logstash, Kibana) para un entorno de prueba de concepto (PoC) con los siguientes componentes:

- **100 servidores web** (500 RPS cada uno)
- **20 servidores de aplicación**
- **10 bases de datos**
- **150 contenedores**

## 🎯 Caso de Estudio

### **Infraestructura Objetivo**
```
🌐 Servidores Web:     100 unidades × 500 RPS = 50,000 RPS total
🔧 Servidores App:     20 unidades × 200 RPS = 4,000 RPS total
🗄️ Bases de Datos:     10 unidades × 100 RPS = 1,000 RPS total
🐳 Contenedores:       150 unidades × 50 RPS = 7,500 RPS total
─────────────────────────────────────────────────────────────
📊 TOTAL:              62,500 RPS (Requests Per Second)
```

### **Políticas de Retención**
- **Logs Críticos**: 90 días
- **Logs Informativos**: 30 días
- **Logs de Debug**: 7 días

## 📈 1. Volumen Diario de Logs

### **Cálculo de Logs por Segundo**

#### **Servidores Web (100 unidades)**
```
📊 RPS por servidor:           500 RPS
📝 Logs por request:           2 logs (access + error)
📊 Total logs/segundo:         100 × 500 × 2 = 100,000 logs/seg
📏 Tamaño promedio por log:    200 bytes
📊 Volumen/segundo:            100,000 × 200 bytes = 20 MB/seg
📊 Volumen/hora:               20 MB/seg × 3,600 = 72 GB/hora
📊 Volumen/día:                72 GB/hora × 24 = 1,728 GB/día
```

#### **Servidores de Aplicación (20 unidades)**
```
📊 RPS por servidor:           200 RPS
📝 Logs por request:           3 logs (info + warn + error)
📊 Total logs/segundo:         20 × 200 × 3 = 12,000 logs/seg
📏 Tamaño promedio por log:    300 bytes
📊 Volumen/segundo:            12,000 × 300 bytes = 3.6 MB/seg
📊 Volumen/hora:               3.6 MB/seg × 3,600 = 12.96 GB/hora
📊 Volumen/día:                12.96 GB/hora × 24 = 311 GB/día
```

#### **Bases de Datos (10 unidades)**
```
📊 RPS por servidor:           100 RPS
📝 Logs por request:           2 logs (query + audit)
📊 Total logs/segundo:         10 × 100 × 2 = 2,000 logs/seg
📏 Tamaño promedio por log:    400 bytes
📊 Volumen/segundo:            2,000 × 400 bytes = 0.8 MB/seg
📊 Volumen/hora:               0.8 MB/seg × 3,600 = 2.88 GB/hora
📊 Volumen/día:                2.88 GB/hora × 24 = 69 GB/día
```

#### **Contenedores (150 unidades)**
```
📊 RPS por contenedor:         50 RPS
📝 Logs por request:           1 log (application)
📊 Total logs/segundo:         150 × 50 × 1 = 7,500 logs/seg
📏 Tamaño promedio por log:    150 bytes
📊 Volumen/segundo:            7,500 × 150 bytes = 1.125 MB/seg
📊 Volumen/hora:               1.125 MB/seg × 3,600 = 4.05 GB/hora
📊 Volumen/día:                4.05 GB/hora × 24 = 97 GB/día
```

### **Resumen de Volumen Diario**
```
🌐 Servidores Web:     1,728 GB/día
🔧 Servidores App:     311 GB/día
🗄️ Bases de Datos:     69 GB/día
🐳 Contenedores:       97 GB/día
─────────────────────────────────────
📊 TOTAL DIARIO:       2,205 GB/día (2.2 TB/día)
📊 TOTAL POR SEGUNDO:  25.525 MB/seg
📊 TOTAL LOGS/SEG:     121,500 logs/segundo
```

## 💾 2. Requerimientos de Storage

### **Cálculo de Storage con Compresión**

#### **Compresión de Elasticsearch**
```
📊 Ratio de compresión:        70% (30% del tamaño original)
📊 Volumen comprimido/día:     2,205 GB × 0.3 = 662 GB/día
📊 Volumen comprimido/mes:     662 GB × 30 = 19,860 GB/mes
```

#### **Storage por Política de Retención**
```
📊 Logs Críticos (90 días):    662 GB/día × 90 = 59,580 GB
📊 Logs Informativos (30 días): 662 GB/día × 30 = 19,860 GB
📊 Logs Debug (7 días):        662 GB/día × 7 = 4,634 GB
─────────────────────────────────────────────────────────
📊 STORAGE TOTAL:              84,074 GB (84 TB)
```

#### **Overhead del Sistema**
```
📊 Índices de Elasticsearch:   20% overhead
📊 Replicas (2x):              100% overhead
📊 Snapshots y backups:        30% overhead
📊 Sistema operativo:          5% overhead
─────────────────────────────────────────────────────────
📊 OVERHEAD TOTAL:             155%
📊 STORAGE FINAL:              84 TB × 2.55 = 214 TB
```

### **Recomendación de Storage**
```
💾 Storage Primario:           250 TB (SSD)
💾 Storage Secundario:         500 TB (HDD)
💾 Storage de Backup:          1,000 TB (Tape/Cloud)
```

## 🖥️ 3. Recursos Computacionales

### **Cálculo de CPU**

#### **Elasticsearch Cluster**
```
📊 Logs por segundo:           121,500 logs/seg
📊 CPU por 1,000 logs/seg:     0.1 CPU cores
📊 CPU base:                   121,500 ÷ 1,000 × 0.1 = 12.15 cores
📊 Factor de seguridad:        2x
📊 CPU total Elasticsearch:    12.15 × 2 = 24.3 cores
📊 Nodos recomendados:         3 nodos × 8 cores = 24 cores
```

#### **Logstash**
```
📊 Logs por segundo:           121,500 logs/seg
📊 CPU por 1,000 logs/seg:     0.05 CPU cores
📊 CPU base:                   121,500 ÷ 1,000 × 0.05 = 6.08 cores
📊 Factor de seguridad:        1.5x
📊 CPU total Logstash:         6.08 × 1.5 = 9.12 cores
📊 Instancias recomendadas:    2 instancias × 5 cores = 10 cores
```

#### **Kibana**
```
📊 Usuarios concurrentes:      50 usuarios
📊 CPU por usuario:            0.1 CPU cores
📊 CPU base:                   50 × 0.1 = 5 cores
📊 Factor de seguridad:        1.5x
📊 CPU total Kibana:           5 × 1.5 = 7.5 cores
📊 Instancias recomendadas:    2 instancias × 4 cores = 8 cores
```

### **Cálculo de RAM**

#### **Elasticsearch Cluster**
```
📊 Datos por día:              662 GB
📊 RAM por GB de datos:        0.5 GB RAM
📊 RAM base:                   662 GB × 0.5 = 331 GB
📊 Factor de seguridad:        1.5x
📊 RAM total Elasticsearch:    331 GB × 1.5 = 496.5 GB
📊 Nodos recomendados:         3 nodos × 170 GB = 510 GB
```

#### **Logstash**
```
📊 Logs por segundo:           121,500 logs/seg
📊 RAM por 1,000 logs/seg:     0.1 GB RAM
📊 RAM base:                   121,500 ÷ 1,000 × 0.1 = 12.15 GB
📊 Factor de seguridad:        2x
📊 RAM total Logstash:         12.15 × 2 = 24.3 GB
📊 Instancias recomendadas:    2 instancias × 15 GB = 30 GB
```

#### **Kibana**
```
📊 Usuarios concurrentes:      50 usuarios
📊 RAM por usuario:            0.2 GB RAM
📊 RAM base:                   50 × 0.2 = 10 GB
📊 Factor de seguridad:        1.5x
📊 RAM total Kibana:           10 × 1.5 = 15 GB
📊 Instancias recomendadas:    2 instancias × 8 GB = 16 GB
```

### **Resumen de Recursos Computacionales**
```
🖥️ CPU Total:                  42 cores
💾 RAM Total:                  556 GB
🖥️ Nodos Elasticsearch:        3 nodos (8 cores, 170 GB RAM c/u)
🔧 Instancias Logstash:        2 instancias (5 cores, 15 GB RAM c/u)
📊 Instancias Kibana:          2 instancias (4 cores, 8 GB RAM c/u)
```

## 🌐 4. Ancho de Banda de Red

### **Cálculo de Ancho de Banda**

#### **Ingesta de Logs**
```
📊 Volumen por segundo:        25.525 MB/seg
📊 Factor de overhead:         1.2x (protocolos, retransmisiones)
📊 Ancho de banda ingesta:     25.525 × 1.2 = 30.63 MB/seg
📊 Ancho de banda ingesta:     30.63 × 8 = 245 Mbps
```

#### **Replicación entre Nodos**
```
📊 Datos por día:              662 GB
📊 Replicación (2x):           662 × 2 = 1,324 GB
📊 Distribución en 24 horas:   1,324 ÷ 24 = 55.17 GB/hora
📊 Ancho de banda replicación: 55.17 ÷ 3,600 × 8 = 0.123 Mbps
```

#### **Consultas y Búsquedas**
```
📊 Usuarios concurrentes:      50 usuarios
📊 Consultas por usuario:      10 consultas/minuto
📊 Tamaño promedio consulta:   1 KB
📊 Ancho de banda consultas:   50 × 10 × 1 KB ÷ 60 × 8 = 66.67 Kbps
```

### **Resumen de Ancho de Banda**
```
📥 Ingesta de Logs:            245 Mbps
🔄 Replicación:                0.123 Mbps
🔍 Consultas:                  0.067 Mbps
─────────────────────────────────────────
📊 TOTAL:                      245.2 Mbps
📊 RECOMENDADO:                1 Gbps (con margen de seguridad)
```

## 🔄 5. Redundancia y Backup

### **Estrategia de Redundancia**

#### **Elasticsearch Cluster**
```
🔄 Replicas por índice:        2 réplicas
🔄 Nodos mínimos:              3 nodos (quorum)
🔄 Tolerancia a fallos:        1 nodo
🔄 Tiempo de recuperación:     < 5 minutos
```

#### **Logstash**
```
🔄 Instancias:                 2 instancias activas
🔄 Balanceador de carga:       HAProxy/Nginx
🔄 Tolerancia a fallos:        1 instancia
🔄 Tiempo de recuperación:     < 2 minutos
```

#### **Kibana**
```
🔄 Instancias:                 2 instancias activas
🔄 Balanceador de carga:       HAProxy/Nginx
🔄 Tolerancia a fallos:        1 instancia
🔄 Tiempo de recuperación:     < 1 minuto
```

### **Estrategia de Backup**

#### **Backup Diario**
```
💾 Frecuencia:                 Diario a las 2:00 AM
💾 Retención:                  30 días
💾 Compresión:                 70% (ratio 3:1)
💾 Tamaño diario:              662 GB × 0.3 = 199 GB
💾 Storage backup:             199 GB × 30 = 5.97 TB
```

#### **Backup Semanal**
```
💾 Frecuencia:                 Semanal (domingos)
💾 Retención:                  12 semanas
💾 Compresión:                 80% (ratio 5:1)
💾 Tamaño semanal:             662 GB × 7 × 0.2 = 927 GB
💾 Storage backup:             927 GB × 12 = 11.12 TB
```

#### **Backup Mensual**
```
💾 Frecuencia:                 Mensual (primer domingo)
💾 Retención:                  12 meses
💾 Compresión:                 85% (ratio 6.7:1)
💾 Tamaño mensual:             662 GB × 30 × 0.15 = 2.98 TB
💾 Storage backup:             2.98 TB × 12 = 35.76 TB
```

### **Resumen de Backup**
```
💾 Backup Diario:              5.97 TB
💾 Backup Semanal:             11.12 TB
💾 Backup Mensual:             35.76 TB
─────────────────────────────────────────
💾 STORAGE BACKUP TOTAL:       52.85 TB
```

## 🏗️ 6. Arquitectura Recomendada

### **Topología del Sistema**
```
┌─────────────────────────────────────────────────────────────┐
│                    Load Balancer (HAProxy)                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┼───────────────────────────────────────┐
│                     │                                       │
│  ┌─────────────────┐│┌─────────────────┐┌─────────────────┐ │
│  │   Kibana-1      │││   Kibana-2      │││   Kibana-3      │ │
│  │   4 cores       │││   4 cores       │││   4 cores       │ │
│  │   8 GB RAM      │││   8 GB RAM      │││   8 GB RAM      │ │
│  └─────────────────┘│└─────────────────┘└─────────────────┘ │
└─────────────────────┼───────────────────────────────────────┘
                      │
┌─────────────────────┼───────────────────────────────────────┐
│                     │                                       │
│  ┌─────────────────┐│┌─────────────────┐┌─────────────────┐ │
│  │   Logstash-1    │││   Logstash-2    │││   Logstash-3    │ │
│  │   5 cores       │││   5 cores       │││   5 cores       │ │
│  │   15 GB RAM     │││   15 GB RAM     │││   15 GB RAM     │ │
│  └─────────────────┘│└─────────────────┘└─────────────────┘ │
└─────────────────────┼───────────────────────────────────────┘
                      │
┌─────────────────────┼───────────────────────────────────────┐
│                     │                                       │
│  ┌─────────────────┐│┌─────────────────┐┌─────────────────┐ │
│  │ Elasticsearch-1 │││ Elasticsearch-2 │││ Elasticsearch-3 │ │
│  │   8 cores       │││   8 cores       │││   8 cores       │ │
│  │   170 GB RAM    │││   170 GB RAM    │││   170 GB RAM    │ │
│  │   250 TB SSD    │││   250 TB SSD    │││   250 TB SSD    │ │
│  └─────────────────┘│└─────────────────┘└─────────────────┘ │
└─────────────────────┼───────────────────────────────────────┘
                      │
┌─────────────────────┼───────────────────────────────────────┐
│                     │                                       │
│  ┌─────────────────┐│┌─────────────────┐┌─────────────────┐ │
│  │   Backup-1      │││   Backup-2      │││   Backup-3      │ │
│  │   500 TB HDD    │││   500 TB HDD    │││   500 TB HDD    │ │
│  └─────────────────┘│└─────────────────┘└─────────────────┘ │
└─────────────────────┼───────────────────────────────────────┘
```

## 💰 7. Estimación de Costos

### **Costos de Hardware (On-Premise)**
```
🖥️ Servidores Elasticsearch:   3 × $15,000 = $45,000
🖥️ Servidores Logstash:        2 × $8,000 = $16,000
🖥️ Servidores Kibana:          2 × $6,000 = $12,000
🖥️ Servidores Backup:          3 × $10,000 = $30,000
🖥️ Load Balancer:              1 × $5,000 = $5,000
💾 Storage SSD:                 750 TB × $0.10/GB = $75,000
💾 Storage HDD:                 1,500 TB × $0.03/GB = $45,000
🌐 Red y Networking:            1 × $10,000 = $10,000
─────────────────────────────────────────────────────────
💰 TOTAL HARDWARE:              $238,000
```

### **Costos de Cloud (AWS)**
```
🖥️ EC2 Instances:              $12,000/mes
💾 EBS Storage:                 $8,000/mes
💾 S3 Storage:                  $3,000/mes
🌐 Data Transfer:               $2,000/mes
🔧 Load Balancer:               $500/mes
─────────────────────────────────────────────────────────
💰 TOTAL CLOUD:                 $25,500/mes
💰 TOTAL ANUAL:                 $306,000
```

## 📋 8. Recomendaciones

### **Implementación Fase 1 (PoC)**
```
🎯 Objetivo:                    Validar funcionalidad
📊 Volumen:                     10% del volumen total
🖥️ Recursos:                   1 nodo Elasticsearch, 1 Logstash, 1 Kibana
💾 Storage:                     25 TB
💰 Costo:                       $25,000
⏱️ Tiempo:                      2 semanas
```

### **Implementación Fase 2 (Producción)**
```
🎯 Objetivo:                    Implementación completa
📊 Volumen:                     100% del volumen total
🖥️ Recursos:                   Arquitectura completa
💾 Storage:                     250 TB
💰 Costo:                       $238,000
⏱️ Tiempo:                      8 semanas
```

### **Consideraciones de Seguridad**
```
🔐 Autenticación:               LDAP/Active Directory
🔐 Autorización:                RBAC (Role-Based Access Control)
🔐 Encriptación:                TLS 1.3 en tránsito
🔐 Encriptación:                AES-256 en reposo
🔐 Auditoría:                   Logs de acceso y modificaciones
```

### **Monitoreo y Alertas**
```
📊 Métricas:                    CPU, RAM, Disk, Network
📊 Alertas:                     Disponibilidad, Latencia, Errores
📊 Dashboards:                  Grafana + Prometheus
📊 Notificaciones:              Email, Slack, PagerDuty
```

## 📊 9. Resumen Ejecutivo

### **Métricas Clave**
```
📊 Volumen diario:              2.2 TB/día
📊 Logs por segundo:            121,500 logs/seg
📊 Storage requerido:           250 TB
📊 CPU total:                   42 cores
📊 RAM total:                   556 GB
📊 Ancho de banda:              1 Gbps
📊 Tiempo de recuperación:      < 5 minutos
```

### **Recomendaciones Finales**
1. **Implementar en fases** para validar funcionalidad
2. **Usar cloud híbrido** para flexibilidad y escalabilidad
3. **Implementar monitoreo** desde el día 1
4. **Planificar backup** y recuperación ante desastres
5. **Capacitar al equipo** en operación y mantenimiento

---

**Este dimensionamiento está basado en las mejores prácticas de la industria y puede ajustarse según los requisitos específicos del entorno.**
