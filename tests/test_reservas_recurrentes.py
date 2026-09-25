from datetime import datetime, timedelta, timezone

from services.reservas_recurrentes import generar_serie
from validators.reservas_recurrentes import validar_creacion


def test_generar_serie_cuatro_semanas():
    zona = timezone(timedelta(hours=-3))

    inicio = datetime(2026, 10, 15, 18, 0, tzinfo=zona)
    fin = datetime(2026, 10, 15, 20, 0, tzinfo=zona)

    serie = generar_serie(inicio, fin, 4)

    assert len(serie) == 4
    assert serie[0]["fecha_hora_inicio"] == inicio
    assert serie[1]["fecha_hora_inicio"] == inicio + timedelta(weeks=1)
    assert serie[3]["fecha_hora_fin"] == fin + timedelta(weeks=3)


def test_validar_creacion_correcta():
    body = {
        "id_socio": 1,
        "id_cancha": 2,
        "fecha_hora_inicio": "2026-10-15T18:00:00.000000-03:00",
        "fecha_hora_fin": "2026-10-15T20:00:00.000000-03:00",
        "cantidad_semanas": 4,
    }

    datos = validar_creacion(body)

    assert datos["id_socio"] == 1
    assert datos["id_cancha"] == 2
    assert datos["cantidad_semanas"] == 4
    assert datos["fecha_hora_inicio"].utcoffset() == timedelta(hours=-3)

import pytest
from errors import ApiError


def test_cantidad_semanas_menor_a_dos():
    body = {
        "id_socio": 1,
        "id_cancha": 2,
        "fecha_hora_inicio": "2026-10-15T18:00:00.000000-03:00",
        "fecha_hora_fin": "2026-10-15T20:00:00.000000-03:00",
        "cantidad_semanas": 1,
    }

    with pytest.raises(ApiError):
        validar_creacion(body)

def test_cantidad_semanas_mayor_a_doce():
    body = {
        "id_socio": 1,
        "id_cancha": 2,
        "fecha_hora_inicio": "2026-10-15T18:00:00.000000-03:00",
        "fecha_hora_fin": "2026-10-15T20:00:00.000000-03:00",
        "cantidad_semanas": 13,
    }

    with pytest.raises(ApiError):
        validar_creacion(body)

def test_fecha_fin_anterior_a_inicio():
    body = {
        "id_socio": 1,
        "id_cancha": 2,
        "fecha_hora_inicio": "2026-10-15T20:00:00.000000-03:00",
        "fecha_hora_fin": "2026-10-15T18:00:00.000000-03:00",
        "cantidad_semanas": 4,
    }

    with pytest.raises(ApiError):
        validar_creacion(body)

def test_zona_horaria_incorrecta():
    body = {
        "id_socio": 1,
        "id_cancha": 2,
        "fecha_hora_inicio": "2026-10-15T18:00:00.000000-04:00",
        "fecha_hora_fin": "2026-10-15T20:00:00.000000-04:00",
        "cantidad_semanas": 4,
    }

    with pytest.raises(ApiError):
        validar_creacion(body)

def test_formato_fecha_invalido():
    body = {
        "id_socio": 1,
        "id_cancha": 2,
        "fecha_hora_inicio": "15/10/2026 18:00",
        "fecha_hora_fin": "2026-10-15T20:00:00.000000-03:00",
        "cantidad_semanas": 4,
    }

    with pytest.raises(ApiError):
        validar_creacion(body)

def test_fecha_sin_microsegundos():
    body = {
        "id_socio": 1,
        "id_cancha": 2,
        "fecha_hora_inicio": "2026-10-15T18:00:00-03:00",
        "fecha_hora_fin": "2026-10-15T20:00:00.000000-03:00",
        "cantidad_semanas": 4,
    }

    with pytest.raises(ApiError):
        validar_creacion(body)