from datetime import datetime, timedelta, timezone

import pytest

from errors import ApiError
from services.reservas import crear_reserva


def test_crear_reserva_calcula_precio_y_conserva_tarifa(monkeypatch):
    zona = timezone(timedelta(hours=-3))
    inicio = datetime(2026, 10, 20, 18, 0, tzinfo=zona)
    fin = datetime(2026, 10, 20, 20, 0, tzinfo=zona)

    monkeypatch.setattr(
        "services.reservas.obtener_cancha",
        lambda id_cancha: {
            "id": id_cancha,
            "activa": True,
            "precio_hora": 1000000,
        },
    )

    monkeypatch.setattr(
        "services.reservas.obtener_socio",
        lambda id_socio: {
            "id": id_socio,
            "activo": True,
        },
    )

    monkeypatch.setattr(
        "services.reservas.validador_reserva_nueva",
        lambda *args: None,
    )

    reserva_guardada = {}

    def crear_fake(reserva):
        reserva_guardada.update(reserva)
        return reserva

    monkeypatch.setattr(
        "services.reservas.repo.crear",
        crear_fake,
    )

    datos = {
        "id_socio": 1,
        "id_cancha": 2,
        "fecha_hora_inicio": inicio,
        "fecha_hora_fin": fin,
    }

    crear_reserva(datos)

    assert reserva_guardada["estado"] == "confirmada"
    assert reserva_guardada["precio_hora"] == 1000000
    assert reserva_guardada["precio_total"] == 2000000


def test_crear_reserva_rechaza_cancha_inactiva(monkeypatch):
    zona = timezone(timedelta(hours=-3))
    inicio = datetime(2026, 10, 20, 18, 0, tzinfo=zona)
    fin = datetime(2026, 10, 20, 20, 0, tzinfo=zona)

    monkeypatch.setattr(
        "services.reservas.obtener_cancha",
        lambda id_cancha: {
            "id": id_cancha,
            "activa": False,
            "precio_hora": 1000000,
        },
    )

    monkeypatch.setattr(
        "services.reservas.obtener_socio",
        lambda id_socio: {
            "id": id_socio,
            "activo": True,
        },
    )

    datos = {
        "id_socio": 1,
        "id_cancha": 2,
        "fecha_hora_inicio": inicio,
        "fecha_hora_fin": fin,
    }

    with pytest.raises(ApiError) as error:
        crear_reserva(datos)

    assert error.value.status == 409
    assert error.value.code == "CANCHA_INACTIVA"


def test_crear_reserva_rechaza_socio_inactivo(monkeypatch):
    zona = timezone(timedelta(hours=-3))
    inicio = datetime(2026, 10, 20, 18, 0, tzinfo=zona)
    fin = datetime(2026, 10, 20, 20, 0, tzinfo=zona)

    monkeypatch.setattr(
        "services.reservas.obtener_cancha",
        lambda id_cancha: {
            "id": id_cancha,
            "activa": True,
            "precio_hora": 1000000,
        },
    )

    monkeypatch.setattr(
        "services.reservas.obtener_socio",
        lambda id_socio: {
            "id": id_socio,
            "activo": False,
        },
    )

    datos = {
        "id_socio": 1,
        "id_cancha": 2,
        "fecha_hora_inicio": inicio,
        "fecha_hora_fin": fin,
    }

    with pytest.raises(ApiError) as error:
        crear_reserva(datos)

    assert error.value.status == 409
    assert error.value.code == "SOCIO_INACTIVO"