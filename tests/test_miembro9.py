import pytest
from app import app

@pytest.fixture
def client ():
    app.confi['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_deportes (client):
    """Verifica que el endpoint de deportes responda HTTP 200"""
    response = client.get('/deportes')
    assert response.status_code == 200

def test_crear_reserva_superpuesta_falla(client):
    """Escenario de prueba: Rechazo de superposicion de reserva (HTTP 409)"""
    reserva_payload = {
        "id_socio": 1,
        "id_cancha": 1,
        "fecha_hora_inicio": "2026-10-15T18:00:00.000000-03:00",
        "fecha_hora_fin": "2026-10-15T20:00:00.000000-03:00"
    }
    # Primera reserva (exito o existente)
    client.post('/reservas', json=reserva_payload)
    # Intento de reserva superpuesta
    response = client.post('/reservas', json=reserva_payload)
    assert response.status_code == 409

def test_borrar_cancha_con_reservas_falla(client):
    """Escenario de prueba: Restriccion al borrar una cancha asociada a una reserva"""
    response = client.delete('/canchas/1')
    assert response.status_code == 409