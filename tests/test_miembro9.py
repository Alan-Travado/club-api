import pytest

from app import app
from errors import ApiError


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_get_deportes(client, monkeypatch):
    monkeypatch.setattr(
        "services.deportes.repo.listar",
        lambda: [
            {"id": 1, "nombre": "Fútbol"},
            {"id": 2, "nombre": "Tenis"},
        ],
    )

    response = client.get("/deportes")

    assert response.status_code == 200


def test_crear_reserva_superpuesta_falla(client, monkeypatch):
    llamadas = {"cantidad": 0}

    def crear_reserva_fake(datos):
        llamadas["cantidad"] += 1

        if llamadas["cantidad"] == 1:
            return {
                "id": 1,
                "id_socio": datos["id_socio"],
                "id_cancha": datos["id_cancha"],
                "fecha_hora_inicio": "2026-10-15T18:00:00.000000-03:00",
                "fecha_hora_fin": "2026-10-15T20:00:00.000000-03:00",
                "estado": "confirmada",
                "precio_hora": 1000000,
                "precio_total": 2000000,
            }

        raise ApiError(
            409,
            "CANCHA_NO_DISPONIBLE",
            "Cancha no disponible",
            "La cancha ya tiene una reserva superpuesta",
        )

    monkeypatch.setattr(
        "routes.reservas.service.crear_reserva",
        crear_reserva_fake,
    )

    reserva_payload = {
        "id_socio": 1,
        "id_cancha": 1,
        "fecha_hora_inicio": "2026-10-15T18:00:00.000000-03:00",
        "fecha_hora_fin": "2026-10-15T20:00:00.000000-03:00",
    }

    primera = client.post("/reservas", json=reserva_payload)
    segunda = client.post("/reservas", json=reserva_payload)

    assert primera.status_code == 201
    assert segunda.status_code == 409


def test_borrar_cancha_con_reservas_falla(client, monkeypatch):
    monkeypatch.setattr(
        "services.canchas.repo.obtener_por_id",
        lambda id_cancha: {
            "id": id_cancha,
            "nombre": "Cancha prueba",
            "id_deporte": 1,
            "precio_hora": 1000000,
            "techada": False,
            "activa": True,
        },
    )

    monkeypatch.setattr(
        "services.canchas.repo.contar_reservas",
        lambda id_cancha: 1,
    )

    response = client.delete("/canchas/1")

    assert response.status_code == 409