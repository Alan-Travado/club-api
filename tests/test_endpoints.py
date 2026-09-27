import pytest

from app import app
from errors import ApiError


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_post_reserva_201(client, monkeypatch):
    def crear_fake(datos):
        return {
            "id": 10,
            "id_socio": datos["id_socio"],
            "id_cancha": datos["id_cancha"],
            "fecha_hora_inicio": "2026-10-20T18:00:00.000000-03:00",
            "fecha_hora_fin": "2026-10-20T20:00:00.000000-03:00",
            "estado": "confirmada",
            "precio_hora": 1000000,
            "precio_total": 2000000,
        }

    monkeypatch.setattr(
        "routes.reservas.service.crear_reserva",
        crear_fake,
    )

    response = client.post(
        "/reservas",
        json={
            "id_socio": 1,
            "id_cancha": 1,
            "fecha_hora_inicio": "2026-10-20T18:00:00.000000-03:00",
            "fecha_hora_fin": "2026-10-20T20:00:00.000000-03:00",
        },
    )

    assert response.status_code == 201
    assert response.get_json()["estado"] == "confirmada"
    assert response.get_json()["precio_total"] == 2000000


def test_get_reserva_200(client, monkeypatch):
    monkeypatch.setattr(
        "routes.reservas.service.obtener_reserva",
        lambda id_reserva: {
            "id": id_reserva,
            "id_socio": 1,
            "id_cancha": 1,
            "estado": "confirmada",
        },
    )

    response = client.get("/reservas/10")

    assert response.status_code == 200
    assert response.get_json()["id"] == 10


def test_get_reserva_404(client, monkeypatch):
    def obtener_fake(id_reserva):
        raise ApiError(
            404,
            "RESERVA_NO_ENCONTRADA",
            "Reserva no encontrada",
            f"No existe una reserva con id {id_reserva}",
        )

    monkeypatch.setattr(
        "routes.reservas.service.obtener_reserva",
        obtener_fake,
    )

    response = client.get("/reservas/9999")

    assert response.status_code == 404


def test_canchas_disponibles_200(client, monkeypatch):
    monkeypatch.setattr(
        "routes.canchas.service.listar_canchas_disponibles",
        lambda filtros, inicio, fin, limit, offset: (
            [
                {
                    "id": 2,
                    "nombre": "Cancha libre",
                    "id_deporte": 1,
                    "precio_hora": 1000000,
                    "techada": False,
                    "activa": True,
                }
            ],
            1,
        ),
    )

    response = client.get(
        "/canchas/disponibles"
        "?fecha=2026-10-20"
        "&hora_inicio=18:00:00"
        "&hora_fin=20:00:00"
    )

    assert response.status_code == 200
    assert len(response.get_json()["canchas"]) == 1
    assert response.get_json()["canchas"][0]["id"] == 2


def test_canchas_disponibles_vacio_devuelve_200(client, monkeypatch):
    monkeypatch.setattr(
        "routes.canchas.service.listar_canchas_disponibles",
        lambda filtros, inicio, fin, limit, offset: ([], 0),
    )

    response = client.get(
        "/canchas/disponibles"
        "?fecha=2026-10-20"
        "&hora_inicio=18:00:00"
        "&hora_fin=20:00:00"
    )

    assert response.status_code == 200
    assert response.get_json()["canchas"] == []