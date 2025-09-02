#!/usr/bin/env python3
"""
Simulador de logs de bases de datos para ELK Stack
Genera logs realistas de MySQL y PostgreSQL cada 5-10 segundos
"""

import random
import time
import json
import socket
import logging
from datetime import datetime, timedelta
from faker import Faker
from colorama import init, Fore, Style

# Inicializar colorama para output colorizado
init()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DatabaseLogSimulator:
    def __init__(self):
        self.fake = Faker()
        self.log_file = "/app/logs/db-logs.log"
        self.tcp_host = "elk-logstash"
        self.tcp_port = 5001
        
        # Tipos de bases de datos
        self.db_types = ["mysql", "postgresql"]
        
        # Niveles de log
        self.log_levels = [
            ("INFO", 0.6),   # 60% información
            ("WARN", 0.25),  # 25% advertencias
            ("ERROR", 0.15)  # 15% errores
        ]
        
        # Queries MySQL comunes
        self.mysql_queries = [
            "SELECT * FROM users WHERE id = ?",
            "INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?)",
            "UPDATE products SET stock = stock - ? WHERE id = ?",
            "DELETE FROM sessions WHERE expires_at < NOW()",
            "SELECT COUNT(*) FROM orders WHERE created_at > ?",
            "SELECT u.name, o.total FROM users u JOIN orders o ON u.id = o.user_id",
            "CREATE INDEX idx_user_email ON users(email)",
            "ALTER TABLE products ADD COLUMN description TEXT",
            "SHOW PROCESSLIST",
            "EXPLAIN SELECT * FROM users WHERE email = ?"
        ]
        
        # Queries PostgreSQL comunes
        self.postgresql_queries = [
            "SELECT * FROM users WHERE id = $1",
            "INSERT INTO orders (user_id, product_id, quantity) VALUES ($1, $2, $3)",
            "UPDATE products SET stock = stock - $1 WHERE id = $2",
            "DELETE FROM sessions WHERE expires_at < NOW()",
            "SELECT COUNT(*) FROM orders WHERE created_at > $1",
            "SELECT u.name, o.total FROM users u JOIN orders o ON u.id = o.user_id",
            "CREATE INDEX CONCURRENTLY idx_user_email ON users(email)",
            "ALTER TABLE products ADD COLUMN description TEXT",
            "SELECT pg_stat_activity()",
            "EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM users WHERE email = $1"
        ]
        
        # Mensajes de error comunes
        self.error_messages = [
            "Connection timeout",
            "Deadlock found when trying to get lock",
            "Table 'database.table' doesn't exist",
            "Duplicate entry for key 'PRIMARY'",
            "Access denied for user",
            "Too many connections",
            "Lock wait timeout exceeded",
            "Column 'column_name' cannot be null",
            "Foreign key constraint fails",
            "Out of memory"
        ]
        
        # Mensajes de advertencia comunes
        self.warning_messages = [
            "Slow query detected",
            "Table scan on large table",
            "Missing index on column",
            "Connection pool nearly exhausted",
            "High memory usage detected",
            "Long running transaction",
            "Inefficient query pattern",
            "Disk space low",
            "Replication lag detected",
            "Cache hit ratio low"
        ]

    def generate_timestamp(self):
        """Genera un timestamp en formato ISO8601"""
        return datetime.now().isoformat()

    def generate_log_level(self):
        """Genera un nivel de log basado en probabilidades"""
        rand = random.random()
        cumulative = 0
        for level, prob in self.log_levels:
            cumulative += prob
            if rand <= cumulative:
                return level
        return "INFO"

    def generate_mysql_log(self, level):
        """Genera un log de MySQL"""
        timestamp = self.generate_timestamp()
        thread_id = random.randint(1000, 9999)
        
        if level == "ERROR":
            message = random.choice(self.error_messages)
        elif level == "WARN":
            message = random.choice(self.warning_messages)
        else:
            query = random.choice(self.mysql_queries)
            duration = random.uniform(0.001, 2.0)
            message = f"Query: {query} | Duration: {duration:.3f}s"
        
        log_line = f"{timestamp} {thread_id} [{level}] {message}"
        
        return {
            "timestamp": timestamp,
            "db_type": "mysql",
            "thread_id": thread_id,
            "level": level,
            "message": message,
            "query": query if level == "INFO" else None,
            "duration": random.uniform(0.001, 2.0) if level == "INFO" else None
        }

    def generate_postgresql_log(self, level):
        """Genera un log de PostgreSQL"""
        timestamp = self.generate_timestamp()
        process_id = random.randint(1000, 9999)
        
        if level == "ERROR":
            message = random.choice(self.error_messages)
        elif level == "WARN":
            message = random.choice(self.warning_messages)
        else:
            query = random.choice(self.postgresql_queries)
            duration = random.uniform(0.001, 2.0)
            message = f"Query: {query} | Duration: {duration:.3f}s"
        
        return {
            "timestamp": timestamp,
            "db_type": "postgresql",
            "process_id": process_id,
            "level": level,
            "message": message,
            "query": query if level == "INFO" else None,
            "duration": random.uniform(0.001, 2.0) if level == "INFO" else None
        }

    def send_to_logstash(self, log_data):
        """Envía el log a Logstash vía TCP"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.tcp_host, self.tcp_port))
                s.sendall((json.dumps(log_data) + '\n').encode('utf-8'))
        except Exception as e:
            logging.error(f"Error enviando a Logstash: {e}")

    def write_to_file(self, log_data):
        """Escribe el log a archivo"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_data) + '\n')
        except Exception as e:
            logging.error(f"Error escribiendo archivo: {e}")

    def run(self):
        """Ejecuta el simulador"""
        logging.info(f"{Fore.GREEN}Iniciando simulador de logs de bases de datos...{Style.RESET_ALL}")
        logging.info(f"Enviando logs a {self.tcp_host}:{self.tcp_port}")
        logging.info(f"Guardando logs en {self.log_file}")
        
        db_count = 0
        
        while True:
            try:
                # Generar logs para múltiples bases de datos (simulando 5 bases de datos)
                for db_id in range(1, 6):
                    db_count += 1
                    db_type = random.choice(self.db_types)
                    level = self.generate_log_level()
                    
                    # Generar 1-2 logs por base de datos
                    for _ in range(random.randint(1, 2)):
                        if db_type == "mysql":
                            log_data = self.generate_mysql_log(level)
                        else:
                            log_data = self.generate_postgresql_log(level)
                        
                        # Agregar identificador de la base de datos
                        log_data["db_instance"] = f"db-{db_id:02d}"
                        log_data["server_id"] = f"db-server-{db_id:02d}"
                        
                        # Enviar a Logstash
                        self.send_to_logstash(log_data)
                        
                        # Escribir a archivo
                        self.write_to_file(log_data)
                        
                        # Log de consola colorizado
                        if level == "ERROR":
                            color = Fore.RED
                        elif level == "WARN":
                            color = Fore.YELLOW
                        else:
                            color = Fore.GREEN
                        
                        print(f"{color}[{datetime.now().strftime('%H:%M:%S')}] {db_type.upper()}-{db_id:02d} [{level}] {log_data['message'][:80]}...{Style.RESET_ALL}")
                
                # Esperar entre 5-10 segundos
                sleep_time = random.uniform(5, 10)
                time.sleep(sleep_time)
                
            except KeyboardInterrupt:
                logging.info(f"{Fore.YELLOW}Deteniendo simulador...{Style.RESET_ALL}")
                break
            except Exception as e:
                logging.error(f"Error en el simulador: {e}")
                time.sleep(5)

if __name__ == "__main__":
    simulator = DatabaseLogSimulator()
    simulator.run()
