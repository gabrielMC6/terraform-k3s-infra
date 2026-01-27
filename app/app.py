from flask import Flask, Response
import prometheus_client
import psycopg2
import os
import time
import random

app = Flask(__name__)

# Define uma métrica do tipo Counter (contador)
REQUEST_COUNT = prometheus_client.Counter('app_requests_total', 'Total de requisicoes recebidas')

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        database=os.environ.get("POSTGRES_DB", "app_db"),
        user=os.environ.get("POSTGRES_USER", "app_user"),
        password=os.environ.get("POSTGRES_PASSWORD", "senha_padrao")
    )

def init_db():
    """Cria a tabela de visitas se não existir"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                id SERIAL PRIMARY KEY,
                count INTEGER NOT NULL DEFAULT 0
            );
        """)
        cur.execute("INSERT INTO visits (id, count) VALUES (1, 0) ON CONFLICT (id) DO NOTHING;")
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao inicializar DB: {e}")

@app.route('/')
def hello():
    # Incrementa o contador toda vez que a home é acessada
    REQUEST_COUNT.inc()
    
    count_msg = ""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE visits SET count = count + 1 WHERE id = 1 RETURNING count;")
        new_count = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        count_msg = f"Total de Acessos: {new_count}"
    except Exception as e:
        count_msg = f"Erro no Banco: {str(e)}"
        
    return f"Ola! Eu sou um app monitorado. Acesse /metrics para ver os dados.<br><br><b>{count_msg}</b>"

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
        conn = get_db_connection()
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
    # Tenta inicializar a tabela no banco
    init_db()
    # Roda na porta 5000
    app.run(host='0.0.0.0', port=5000)