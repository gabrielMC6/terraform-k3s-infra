FROM python:3.9-slim
WORKDIR /app
RUN pip install flask prometheus_client psycopg2-binary
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]