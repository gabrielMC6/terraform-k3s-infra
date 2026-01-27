import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Testa se a rota home responde corretamente"""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Ola! Eu sou um app monitorado" in rv.data

def test_metrics(client):
    """Testa se a rota de metricas esta expondo dados"""
    rv = client.get('/metrics')
    assert rv.status_code == 200
    assert b"app_requests_total" in rv.data