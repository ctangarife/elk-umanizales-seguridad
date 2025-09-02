#!/usr/bin/env python3
"""
Simulador de logs de microservicios para ELK Stack
Genera logs JSON estructurados con trace IDs cada 5-10 segundos
"""

import random
import time
import json
import socket
import logging
import uuid
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

class MicroserviceLogSimulator:
    def __init__(self):
        self.fake = Faker()
        self.log_file = "/app/logs/micro-logs.log"
        self.tcp_host = "elk-logstash"
        self.tcp_port = 5002
        
        # Microservicios simulados
        self.services = [
            "user-service", "auth-service", "payment-service", "order-service",
            "inventory-service", "notification-service", "analytics-service",
            "gateway-service", "config-service", "monitoring-service"
        ]
        
        # Niveles de log
        self.log_levels = [
            ("INFO", 0.5),   # 50% información
            ("DEBUG", 0.25), # 25% debug
            ("WARN", 0.15),  # 15% advertencias
            ("ERROR", 0.1)   # 10% errores
        ]
        
        # Endpoints de microservicios
        self.endpoints = {
            "user-service": ["/users", "/users/{id}", "/users/{id}/profile", "/users/search"],
            "auth-service": ["/auth/login", "/auth/logout", "/auth/refresh", "/auth/validate"],
            "payment-service": ["/payments", "/payments/{id}", "/payments/process", "/payments/refund"],
            "order-service": ["/orders", "/orders/{id}", "/orders/{id}/status", "/orders/history"],
            "inventory-service": ["/products", "/products/{id}", "/products/search", "/products/stock"],
            "notification-service": ["/notifications", "/notifications/send", "/notifications/templates"],
            "analytics-service": ["/analytics/events", "/analytics/metrics", "/analytics/reports"],
            "gateway-service": ["/gateway/routes", "/gateway/health", "/gateway/metrics"],
            "config-service": ["/config", "/config/{service}", "/config/reload"],
            "monitoring-service": ["/health", "/metrics", "/alerts", "/dashboards"]
        }
        
        # Mensajes de error comunes
        self.error_messages = [
            "Database connection failed",
            "External service timeout",
            "Invalid request payload",
            "Authentication failed",
            "Rate limit exceeded",
            "Service unavailable",
            "Configuration error",
            "Memory allocation failed",
            "Network timeout",
            "Validation error"
        ]
        
        # Mensajes de advertencia comunes
        self.warning_messages = [
            "High response time detected",
            "Cache miss rate high",
            "Deprecated API usage",
            "Resource usage high",
            "Slow database query",
            "External service slow",
            "Memory usage approaching limit",
            "Connection pool nearly exhausted",
            "Retry attempt failed",
            "Circuit breaker open"
        ]
        
        # Mensajes de información comunes
        self.info_messages = [
            "Request processed successfully",
            "User authenticated",
            "Payment processed",
            "Order created",
            "Product updated",
            "Notification sent",
            "Analytics event recorded",
            "Configuration updated",
            "Health check passed",
            "Metrics collected"
        ]

    def generate_timestamp(self):
        """Genera un timestamp en formato ISO8601"""
        return datetime.now().isoformat()

    def generate_trace_id(self):
        """Genera un trace ID único"""
        return str(uuid.uuid4())

    def generate_span_id(self):
        """Genera un span ID único"""
        return str(uuid.uuid4())[:8]

    def generate_log_level(self):
        """Genera un nivel de log basado en probabilidades"""
        rand = random.random()
        cumulative = 0
        for level, prob in self.log_levels:
            cumulative += prob
            if rand <= cumulative:
                return level
        return "INFO"

    def generate_microservice_log(self, service):
        """Genera un log de microservicio"""
        timestamp = self.generate_timestamp()
        level = self.generate_log_level()
        trace_id = self.generate_trace_id()
        span_id = self.generate_span_id()
        
        # Generar mensaje basado en el nivel
        if level == "ERROR":
            message = random.choice(self.error_messages)
            error = {
                "type": "ServiceError",
                "message": message,
                "stack_trace": f"Error in {service} at {timestamp}"
            }
        elif level == "WARN":
            message = random.choice(self.warning_messages)
            error = None
        elif level == "DEBUG":
            message = f"Debug info for {service}"
            error = None
        else:
            message = random.choice(self.info_messages)
            error = None
        
        # Generar endpoint si es un servicio HTTP
        endpoint = None
        if service in self.endpoints:
            endpoint = random.choice(self.endpoints[service])
        
        # Generar duración de respuesta
        duration = random.uniform(0.001, 5.0)
        
        # Generar métricas adicionales
        metrics = {
            "cpu_usage": random.uniform(10, 90),
            "memory_usage": random.uniform(20, 80),
            "response_time": duration,
            "requests_per_second": random.uniform(10, 1000)
        }
        
        log_data = {
            "timestamp": timestamp,
            "level": level,
            "service": service,
            "message": message,
            "trace_id": trace_id,
            "span_id": span_id,
            "endpoint": endpoint,
            "duration": duration,
            "metrics": metrics,
            "environment": "production",
            "version": f"1.{random.randint(0, 9)}.{random.randint(0, 9)}"
        }
        
        if error:
            log_data["error"] = error
        
        return log_data

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
        logging.info(f"{Fore.GREEN}Iniciando simulador de logs de microservicios...{Style.RESET_ALL}")
        logging.info(f"Enviando logs a {self.tcp_host}:{self.tcp_port}")
        logging.info(f"Guardando logs en {self.log_file}")
        
        service_count = 0
        
        while True:
            try:
                # Generar logs para múltiples microservicios (simulando 10 microservicios)
                for service_id in range(1, 11):
                    service_count += 1
                    service = random.choice(self.services)
                    
                    # Generar 1-3 logs por microservicio
                    for _ in range(random.randint(1, 3)):
                        log_data = self.generate_microservice_log(service)
                        
                        # Agregar identificador de instancia
                        log_data["instance_id"] = f"{service}-{service_id:02d}"
                        log_data["pod_name"] = f"{service}-pod-{service_id:02d}"
                        
                        # Enviar a Logstash
                        self.send_to_logstash(log_data)
                        
                        # Escribir a archivo
                        self.write_to_file(log_data)
                        
                        # Log de consola colorizado
                        if log_data["level"] == "ERROR":
                            color = Fore.RED
                        elif log_data["level"] == "WARN":
                            color = Fore.YELLOW
                        elif log_data["level"] == "DEBUG":
                            color = Fore.BLUE
                        else:
                            color = Fore.GREEN
                        
                        print(f"{color}[{datetime.now().strftime('%H:%M:%S')}] {service.upper()}-{service_id:02d} [{log_data['level']}] {log_data['message'][:60]}...{Style.RESET_ALL}")
                
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
    simulator = MicroserviceLogSimulator()
    simulator.run()
