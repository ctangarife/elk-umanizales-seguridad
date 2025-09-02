#!/usr/bin/env python3
"""
Simulador de logs de servidores web para ELK Stack
Genera logs realistas de Apache/Nginx cada 5-10 segundos
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

class WebLogSimulator:
    def __init__(self):
        self.fake = Faker()
        self.log_file = "/app/logs/web-logs.log"
        self.tcp_host = "elk-logstash"
        self.tcp_port = 5000
        
        # Lista de métodos HTTP
        self.http_methods = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]
        
        # Lista de endpoints comunes
        self.endpoints = [
            "/", "/index.html", "/about", "/contact", "/products", "/services",
            "/api/users", "/api/products", "/api/orders", "/api/auth/login",
            "/api/auth/logout", "/admin", "/dashboard", "/profile", "/settings",
            "/search", "/cart", "/checkout", "/payment", "/confirmation"
        ]
        
        # Lista de códigos de respuesta HTTP con probabilidades
        self.status_codes = [
            (200, 0.7),   # 70% éxito
            (201, 0.05),  # 5% creado
            (301, 0.03),  # 3% redirección permanente
            (302, 0.02),  # 2% redirección temporal
            (400, 0.05),  # 5% error del cliente
            (401, 0.03),  # 3% no autorizado
            (403, 0.02),  # 2% prohibido
            (404, 0.08),  # 8% no encontrado
            (500, 0.015), # 1.5% error del servidor
            (502, 0.005), # 0.5% bad gateway
            (503, 0.005)  # 0.5% servicio no disponible
        ]
        
        # User agents realistas
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59"
        ]
        
        # Referrers comunes
        self.referrers = [
            "-", "https://www.google.com/", "https://www.bing.com/", "https://www.yahoo.com/",
            "https://www.facebook.com/", "https://www.twitter.com/", "https://www.linkedin.com/",
            "https://github.com/", "https://stackoverflow.com/"
        ]

    def generate_ip(self):
        """Genera una IP realista"""
        return self.fake.ipv4()

    def generate_timestamp(self):
        """Genera un timestamp en formato Apache"""
        now = datetime.now()
        return now.strftime("%d/%b/%Y:%H:%M:%S +0000")

    def generate_status_code(self):
        """Genera un código de estado HTTP basado en probabilidades"""
        rand = random.random()
        cumulative = 0
        for status, prob in self.status_codes:
            cumulative += prob
            if rand <= cumulative:
                return status
        return 200

    def generate_bytes(self, status_code):
        """Genera el tamaño de respuesta en bytes"""
        if status_code >= 400:
            return random.randint(0, 1000)  # Errores suelen ser más pequeños
        elif status_code in [301, 302]:
            return random.randint(0, 500)   # Redirecciones pequeñas
        else:
            return random.randint(100, 50000)  # Respuestas normales

    def generate_apache_log(self):
        """Genera un log en formato Apache Common Log Format"""
        ip = self.generate_ip()
        timestamp = self.generate_timestamp()
        method = random.choice(self.http_methods)
        endpoint = random.choice(self.endpoints)
        http_version = "1.1"
        status = self.generate_status_code()
        bytes_size = self.generate_bytes(status)
        referrer = random.choice(self.referrers)
        user_agent = random.choice(self.user_agents)
        
        # Formato Apache Common Log Format
        log_line = f'{ip} - - [{timestamp}] "{method} {endpoint} HTTP/{http_version}" {status} {bytes_size} "{referrer}" "{user_agent}"'
        
        return log_line

    def send_to_logstash(self, log_line):
        """Envía el log a Logstash vía TCP"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.tcp_host, self.tcp_port))
                s.sendall((log_line + '\n').encode('utf-8'))
        except Exception as e:
            logging.error(f"Error enviando a Logstash: {e}")

    def write_to_file(self, log_line):
        """Escribe el log a archivo"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_line + '\n')
        except Exception as e:
            logging.error(f"Error escribiendo archivo: {e}")

    def run(self):
        """Ejecuta el simulador"""
        logging.info(f"{Fore.GREEN}Iniciando simulador de logs de servidores web...{Style.RESET_ALL}")
        logging.info(f"Enviando logs a {self.tcp_host}:{self.tcp_port}")
        logging.info(f"Guardando logs en {self.log_file}")
        
        server_count = 0
        
        while True:
            try:
                # Generar logs para múltiples servidores (simulando 50 servidores)
                for server_id in range(1, 51):
                    server_count += 1
                    
                    # Generar 1-3 logs por servidor
                    for _ in range(random.randint(1, 3)):
                        log_line = self.generate_apache_log()
                        
                        # Agregar identificador del servidor
                        log_line = f"[Server-{server_id:02d}] {log_line}"
                        
                        # Enviar a Logstash
                        self.send_to_logstash(log_line)
                        
                        # Escribir a archivo
                        self.write_to_file(log_line)
                        
                        # Log de consola colorizado
                        status = log_line.split('"')[1].split()[1] if '"' in log_line else "200"
                        if status.startswith('2'):
                            color = Fore.GREEN
                        elif status.startswith('3'):
                            color = Fore.YELLOW
                        elif status.startswith('4'):
                            color = Fore.RED
                        else:
                            color = Fore.MAGENTA
                        
                        print(f"{color}[{datetime.now().strftime('%H:%M:%S')}] Server-{server_id:02d} - {log_line[:100]}...{Style.RESET_ALL}")
                
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
    simulator = WebLogSimulator()
    simulator.run()
