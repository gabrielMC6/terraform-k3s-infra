from flask import Flask, Response
import prometheus_client
import psycopg2
import os
import time
import random

app = Flask(__name__)

# Define uma métrica do tipo Counter (contador)
REQUEST_COUNT = prometheus_client.Counter('app_requests_total', 'Total de requisicoes recebidas')

@app.route('/')
def hello():
    # Incrementa o contador toda vez que a home é acessada
    REQUEST_COUNT.inc()
    return "Ola! Eu sou um app monitorado. Acesse /metrics para ver os dados."

@app.route('/db')
def db_check():
    try:
        # Pega as credenciais das variaveis de ambiente (que o K8s vai injetar)
        conn = psycopg2.connect(
            host=os.environ.get("POSTGRES_HOST", "localhost"),
            database=os.environ.get("POSTGRES_DB", "app_db"),
            user=os.environ.get("POSTGRES_USER", "app_user"),
            password=os.environ.get("POSTGRES_PASSWORD", "senha_padrao")
        )
        cur = conn.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        conn.close()
        return f"Conexão com Banco de Dados: SUCESSO! <br> Versão: {db_version[0]}"
    except Exception as e:
        return f"Erro ao conectar no banco: {str(e)}", 500

@app.route('/metrics')
def metrics():
    # Rota padrão que o Prometheus usa para coletar dados
    return Response(prometheus_client.generate_latest(), mimetype="text/plain")

if __name__ == '__main__':
    # Roda na porta 5000
    app.run(host='0.0.0.0', port=5000)