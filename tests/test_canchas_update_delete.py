import pytest

from errors import ApiError
from services import canchas as service
from validators import canchas as validador


def test_validar_actualizacion_cancha_valida():
    body = {
        "nombre": "Cancha editada",
        "precio_hora": 1800000,
        "techada": True,
        "activa": False,
    }

    datos = validador.validar_actualizacion(body)

    assert datos == body


def test_validar_actualizacion_rechaza_id_deporte():
    with pytest.raises(ApiError) as error:
        validador.validar_actualizacion({
            "id_deporte": 2
        })

    assert error.value.status == 400


def test_validar_actualizacion_rechaza_body_vacio():
    with pytest.raises(ApiError) as error:
        validador.validar_actualizacion({})

    assert error.value.status == 400


def test_actualizar_cancha_inexistente(monkeypatch):
    monkeypatch.setattr(
        "services.canchas.repo.obtener_por_id",
        lambda id_cancha: None,
    )

    with pytest.raises(ApiError) as error:
        service.actualizar_cancha(
            9999,
            {"activa": False},
        )

    assert error.value.status == 404


def test_eliminar_cancha_con_reservas(monkeypatch):
    monkeypatch.setattr(
        "services.canchas.repo.obtener_por_id",
        lambda id_cancha: {
            "id": id_cancha,
            "nombre": "Cancha prueba",
        },
    )

    monkeypatch.setattr(
        "services.canchas.repo.contar_reservas",
        lambda id_cancha: 2,
    )

    with pytest.raises(ApiError) as error:
        service.eliminar_cancha(1)

    assert error.value.status == 409
    assert error.value.code == "CANCHA_CON_RESERVAS"


def test_eliminar_cancha_sin_reservas(monkeypatch):
    eliminadas = []

    monkeypatch.setattr(
        "services.canchas.repo.obtener_por_id",
        lambda id_cancha: {
            "id": id_cancha,
            "nombre": "Cancha prueba",
        },
    )

    monkeypatch.setattr(
        "services.canchas.repo.contar_reservas",
        lambda id_cancha: 0,
    )

    monkeypatch.setattr(
        "services.canchas.repo.eliminar",
        lambda id_cancha: eliminadas.append(id_cancha),
    )

    service.eliminar_cancha(6)

    assert eliminadas == [6]