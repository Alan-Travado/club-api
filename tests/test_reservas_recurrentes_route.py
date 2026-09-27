from flask import Flask

from errors import ApiError, registrar_manejadores
from routes.reservas_recurrentes import bp
from datetime import datetime, timedelta, timezone

def test_post_reservas_recurrentes_devuelve_201(monkeypatch):
    app = Flask(__name__)

    registrar_manejadores(app)
    app.register_blueprint(bp)

    reservas_creadas = [
        {"id": 1},
        {"id": 2},
        {"id": 3},
        {"id": 4},
    ]

    monkeypatch.setattr(
        "routes.reservas_recurrentes."
        "service.crear_reservas_recurrentes",
        lambda datos: reservas_creadas,
    )

    client = app.test_client()

    respuesta = client.post(
        "/reservas/recurrentes",
        json={
            "id_socio": 1,
            "id_cancha": 2,
            "fecha_hora_inicio":
                "2026-10-15T18:00:00.000000-03:00",
            "fecha_hora_fin":
                "2026-10-15T20:00:00.000000-03:00",
            "cantidad_semanas": 4,
        },
    )

    body = respuesta.get_json()

    assert respuesta.status_code == 201
    assert len(body["reservas"]) == 4
    assert body["reservas"][0]["id"] == 1

def test_post_reservas_recurrentes_devuelve_409_con_conflictos(monkeypatch):
    app = Flask(__name__)

    registrar_manejadores(app)
    app.register_blueprint(bp)

    def service_con_conflicto(datos):
        raise ApiError(
            409,
            "RESERVAS_NO_DISPONIBLES",
            "Conflicto en la serie de reservas",
            "Una o más fechas no están disponibles",
            conflictos=[
                "2026-10-22",
                "2026-11-05",
            ],
        )

    monkeypatch.setattr(
        "routes.reservas_recurrentes."
        "service.crear_reservas_recurrentes",
        service_con_conflicto,
    )

    client = app.test_client()

    respuesta = client.post(
        "/reservas/recurrentes",
        json={
            "id_socio": 1,
            "id_cancha": 2,
            "fecha_hora_inicio":
                "2026-10-15T18:00:00.000000-03:00",
            "fecha_hora_fin":
                "2026-10-15T20:00:00.000000-03:00",
            "cantidad_semanas": 4,
        },
    )

    body = respuesta.get_json()

    assert respuesta.status_code == 409
    assert body["conflictos"] == [
        "2026-10-22",
        "2026-11-05",
    ]
    assert body["errors"][0]["code"] == "RESERVAS_NO_DISPONIBLES"

def test_post_reservas_recurrentes_formato_fechas(monkeypatch):
    app = Flask(__name__)

    registrar_manejadores(app)
    app.register_blueprint(bp)

    zona = timezone(timedelta(hours=-3))

    reservas_creadas = [
        {
            "id": 1,
            "id_socio": 1,
            "id_cancha": 2,
            "fecha_hora_inicio": datetime(
                2026, 10, 15, 18, 0, tzinfo=zona
            ),
            "fecha_hora_fin": datetime(
                2026, 10, 15, 20, 0, tzinfo=zona
            ),
            "estado": "confirmada",
            "precio_hora": 1000000,
            "precio_total": 2000000,
        }
    ]

    monkeypatch.setattr(
        "routes.reservas_recurrentes."
        "service.crear_reservas_recurrentes",
        lambda datos: reservas_creadas,
    )

    client = app.test_client()

    respuesta = client.post(
        "/reservas/recurrentes",
        json={
            "id_socio": 1,
            "id_cancha": 2,
            "fecha_hora_inicio":
                "2026-10-15T18:00:00.000000-03:00",
            "fecha_hora_fin":
                "2026-10-15T20:00:00.000000-03:00",
            "cantidad_semanas": 2,
        },
    )

    body = respuesta.get_json()

    assert body["reservas"][0]["fecha_hora_inicio"] == (
        "2026-10-15T18:00:00.000000-03:00"
    )
