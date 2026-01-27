FROM python:3.9-slim
WORKDIR /app
# Atualiza pip, setuptools e wheel para corrigir vulnerabilidades críticas
RUN pip install --upgrade pip setuptools wheel
# Instala dependências do sistema e bibliotecas Python
RUN pip install flask prometheus_client psycopg2-binary
COPY app.py .
# Expõe a porta da aplicação para o container
EXPOSE 5000
CMD ["python", "app.py"]