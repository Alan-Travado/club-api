import pytest

from errors import ApiError
from datetime import datetime, timedelta, timezone
from services.disponibilidad import validador_reserva_nueva


def test_validador_reserva_nueva_sin_conflictos(monkeypatch):
    zona = timezone(timedelta(hours=-3))

    inicio = datetime(2026, 10, 15, 18, 0, tzinfo=zona)
    fin = datetime(2026, 10, 15, 20, 0, tzinfo=zona)

    monkeypatch.setattr(
        "services.disponibilidad.repo_reservas.existe_superposicion_en_cancha",
        lambda *args: False,
    )

    monkeypatch.setattr(
        "services.disponibilidad.repo_reservas.existe_superposicion_en_socio",
        lambda *args: False,
    )

    monkeypatch.setattr(
    "services.disponibilidad.repo_reservas.existe_superposicion_en_bloqueo",
    lambda *args: False,
)

    validador_reserva_nueva(
        2,
        1,
        inicio,
        fin,
    )

def test_validador_reserva_conflicto_cancha(monkeypatch):
    zona = timezone(timedelta(hours=-3))
    inicio = datetime(2026, 10, 15, 18, 0, tzinfo=zona)
    fin = datetime(2026, 10, 15, 20, 0, tzinfo=zona)

    monkeypatch.setattr(
        "services.disponibilidad.repo_reservas.existe_superposicion_en_cancha",
        lambda *args: True,
    )

    with pytest.raises(ApiError) as error:
        validador_reserva_nueva(2, 1, inicio, fin)

    assert error.value.status == 409
    assert error.value.code == "CANCHA_NO_DISPONIBLE"


def test_validador_reserva_conflicto_socio(monkeypatch):
    zona = timezone(timedelta(hours=-3))
    inicio = datetime(2026, 10, 15, 18, 0, tzinfo=zona)
    fin = datetime(2026, 10, 15, 20, 0, tzinfo=zona)

    monkeypatch.setattr(
        "services.disponibilidad.repo_reservas.existe_superposicion_en_cancha",
        lambda *args: False,
    )
    monkeypatch.setattr(
        "services.disponibilidad.repo_reservas.existe_superposicion_en_socio",
        lambda *args: True,
    )

    with pytest.raises(ApiError) as error:
        validador_reserva_nueva(2, 1, inicio, fin)

    assert error.value.status == 409
    assert error.value.code == "SOCIO_NO_DISPONIBLE"

def test_validador_reserva_conflicto_bloqueo(monkeypatch):
    zona = timezone(timedelta(hours=-3))
    inicio = datetime(2026, 10, 15, 18, 0, tzinfo=zona)
    fin = datetime(2026, 10, 15, 20, 0, tzinfo=zona)

    monkeypatch.setattr(
        "services.disponibilidad.repo_reservas.existe_superposicion_en_cancha",
        lambda *args: False,
    )
    monkeypatch.setattr(
        "services.disponibilidad.repo_reservas.existe_superposicion_en_socio",
        lambda *args: False,
    )
    monkeypatch.setattr(
        "services.disponibilidad.repo_reservas.existe_superposicion_en_bloqueo",
        lambda *args: True,
    )

    with pytest.raises(ApiError) as error:
        validador_reserva_nueva(2, 1, inicio, fin)

    assert error.value.status == 409
    assert error.value.code == "CANCHA_NO_DISPONIBLE"