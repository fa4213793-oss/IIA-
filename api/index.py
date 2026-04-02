from http.server import BaseHTTPRequestHandler
import json
import time
import random
import os
from upstash_redis import Redis

# Configuração da Memória (O bot usa as variáveis que vais colocar no Vercel)
redis = Redis(
    url=os.environ.get("UPSTASH_REDIS_REST_URL"), 
    token=os.environ.get("UPSTASH_REDIS_REST_TOKEN")
)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        # 1. CÁLCULO DE LATÊNCIA (Compensação Angola-Europa)
        client_time = data.get('timestamp', time.time() * 1000)
        server_time = time.time() * 1000
        latency = server_time - client_time

        # 2. CONSULTA À MEMÓRIA (O que o Deus já aprendeu)
        game_type = data.get('gameType', 'default')
        last_pattern = redis.get(f"pattern_{game_type}")

        # 3. LÓGICA DE DECISÃO
        # Aqui o cérebro decide se o padrão atual é vencedor
        probability = random.randint(10, 95) # Simulação de IA
        action = "WAIT"
        
        if probability > 80:
            action = "EXECUTE_CLIQUE"

        # 4. HUMANIZAÇÃO (Evitar Ban)
        # Adiciona um atraso aleatório entre 150ms e 300ms
        human_delay = random.uniform(150, 300)

        response = {
            "instruction": action,
            "confidence": probability,
            "delay_ms": max(0, human_delay - latency),
            "coords": {"x": 540 + random.randint(-5, 5), "y": 960 + random.randint(-5, 5)}
        }

        # 5. EVOLUÇÃO (Gravar para a próxima rodada)
        redis.set(f"last_action_{game_type}", action)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
        return