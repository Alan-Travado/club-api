from datetime import datetime, timedelta, timezone
from services.reservas_recurrentes import generar_serie, detectar_conflictos
from validators.reservas_recurrentes import validar_creacion
from services.reservas_recurrentes import (
    generar_serie,
    detectar_conflictos,
    validar_recursos,
    preparar_serie,
    completar_reservas,
    construir_reservas,
    crear_reservas_recurrentes,
)

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

def test_detectar_varios_conflictos(monkeypatch):
    zona = timezone(timedelta(hours=-3))

    inicio = datetime(2026, 10, 15, 18, 0, tzinfo=zona)
    fin = datetime(2026, 10, 15, 20, 0, tzinfo=zona)

    serie = generar_serie(inicio, fin, 4)

    fechas_conflicto = {
        "2026-10-22",
        "2026-11-05",
    }

    def fake_validar_reserva_nueva(id_cancha, id_socio, inicio, fin):
        if inicio.date().isoformat() in fechas_conflicto:
            raise ApiError(
                409,
                "CANCHA_NO_DISPONIBLE",
                "Cancha no disponible",
                "Conflicto de prueba",
            )

    monkeypatch.setattr(
        "services.reservas_recurrentes.validar_reserva_nueva",
        fake_validar_reserva_nueva
    )

    conflictos = detectar_conflictos(
        2,
        1,
        serie
    )

    assert conflictos == [
        "2026-10-22",
        "2026-11-05",
    ]

def test_detectar_sin_conflictos(monkeypatch):
    zona = timezone(timedelta(hours=-3))

    inicio = datetime(2026, 10, 15, 18, 0, tzinfo=zona)
    fin = datetime(2026, 10, 15, 20, 0, tzinfo=zona)

    serie = generar_serie(inicio, fin, 4)

    def fake_validar_reserva_nueva(id_cancha, id_socio, inicio, fin):
        return None

    monkeypatch.setattr(
        "services.reservas_recurrentes.validar_reserva_nueva",
        fake_validar_reserva_nueva
    )

    conflictos = detectar_conflictos(
        2,
        1,
        serie
    )

    assert conflictos == []

def test_validar_recursos_correctos(monkeypatch):
    monkeypatch.setattr(
        "services.reservas_recurrentes.obtener_cancha",
        lambda id_cancha: {
            "id": id_cancha,
            "activa": True
        },
    )

    monkeypatch.setattr(
        "services.reservas_recurrentes.obtener_socio",
        lambda id_socio: {
            "id": id_socio,
            "activo": True
        },
    )

    cancha, socio = validar_recursos(2, 1)
    assert cancha["id"] == 2
    assert socio["id"] == 1

def test_validar_recursos_cancha_inactiva(monkeypatch):
    monkeypatch.setattr(
        "services.reservas_recurrentes.obtener_cancha",
        lambda id_cancha: {
            "id": id_cancha,
            "activa": False
        },
    )

    monkeypatch.setattr(
        "services.reservas_recurrentes.obtener_socio",
        lambda id_socio: {
            "id": id_socio,
            "activo": True
        },
    )

    with pytest.raises(ApiError) as error:
        validar_recursos(2, 1)
    assert error.value.status == 409
    assert error.value.code == "CANCHA_INACTIVA"

def test_validar_recursos_socio_inactivo(monkeypatch):
    monkeypatch.setattr(
        "services.reservas_recurrentes.obtener_cancha",
        lambda id_cancha: {
            "id": id_cancha,
            "activa": True
        },
    )

    monkeypatch.setattr(
        "services.reservas_recurrentes.obtener_socio",
        lambda id_socio: {
            "id": id_socio,
            "activo": False
        },
    )

    with pytest.raises(ApiError) as error:
        validar_recursos(2, 1)
    assert error.value.status == 409
    assert error.value.code == "SOCIO_INACTIVO"

def test_preparar_serie(monkeypatch):
    zona = timezone(timedelta(hours=-3))

    datos = {
        "id_socio": 1,
        "id_cancha": 2,
        "fecha_hora_inicio": datetime(2026, 10, 15, 18, 0, tzinfo=zona),
        "fecha_hora_fin": datetime(2026, 10, 15, 20, 0, tzinfo=zona),
        "cantidad_semanas": 4,
    }

    monkeypatch.setattr(
        "services.reservas_recurrentes.validar_recursos",
        lambda *args: (
            {"id": 2, "activa": True},
            {"id": 1, "activo": True},
        ),
    )

    monkeypatch.setattr(
        "services.reservas_recurrentes.detectar_conflictos",
        lambda *args: [
            "2026-10-22",
            "2026-11-05",
        ],
    )

    with pytest.raises(ApiError) as error:
        preparar_serie(datos)

        assert error.value.status == 409
        assert error.value.conflictos == [
            "2026-10-22",
            "2026-11-05",
        ]

def test_preparar_serie_sin_conflictos(monkeypatch):
    zona = timezone(timedelta(hours=-3))

    datos = {
        "id_socio": 1,
        "id_cancha": 2,
        "fecha_hora_inicio": datetime(2026, 10, 15, 18, 0, tzinfo=zona),
        "fecha_hora_fin": datetime(2026, 10, 15, 20, 0, tzinfo=zona),
        "cantidad_semanas": 4,
    }

    cancha_falsa = {
        "id": 2,
        "activa": True,
        "precio_hora": 1000000,
    }

    socio_falso = {
        "id": 1,
        "activo": True,
    }

    monkeypatch.setattr(
        "services.reservas_recurrentes.validar_recursos",
        lambda *args: (cancha_falsa, socio_falso),
    )

    monkeypatch.setattr(
        "services.reservas_recurrentes.detectar_conflictos",
        lambda *args: [],
    )

    cancha, socio, serie = preparar_serie(datos)

    assert cancha == cancha_falsa
    assert socio == socio_falso
    assert len(serie) == 4

    assert serie[0]["fecha_hora_inicio"] == datos["fecha_hora_inicio"]
    assert serie[3]["fecha_hora_inicio"] == (datos["fecha_hora_inicio"] + timedelta(weeks=3))

def test_completar_reservas_calcula_precio():
    zona = timezone(timedelta(hours=-3))

    cancha = {
        "id": 2,
        "activa": True,
        "precio_hora": 1000000,
    }

    socio = {
        "id": 1,
    }

    serie = generar_serie(
        datetime(2026, 10, 15, 18, 0, tzinfo=zona),
        datetime(2026, 10, 15, 20, 0, tzinfo=zona),
        4
    )

    reservas = completar_reservas(cancha, socio, serie)

    assert len(reservas) == 4
    assert reservas[0]["id_socio"] == 1
    assert reservas[0]["id_cancha"] == 2
    assert reservas[0]["estado"] == "confirmada"
    assert reservas[0]["precio_hora"] == 1000000
    assert reservas[0]["precio_total"] == 2000000

def test_construir_reservas(monkeypatch):
    zona = timezone(timedelta(hours=-3))

    datos = {
        "id_socio": 1,
        "id_cancha": 2,
        "fecha_hora_inicio": datetime(2026, 10, 15, 18, 0, tzinfo=zona),
        "fecha_hora_fin": datetime(2026, 10, 15, 20, 0, tzinfo=zona),
        "cantidad_semanas": 4,
    }

    cancha = {
        "id": 2,
        "activa": True,
        "precio_hora": 1000000,
    }
    
    socio = {
        "id": 1,
        "activo": True,
    }
    
    serie = generar_serie(
        datos["fecha_hora_inicio"],
        datos["fecha_hora_fin"],
        4,
    )

    monkeypatch.setattr(
        "services.reservas_recurrentes.preparar_serie",
        lambda datos: (cancha, socio, serie),
    )

    reservas = construir_reservas(datos)

    assert len(reservas) == 4
    assert reservas[0]["estado"] == "confirmada"
    assert reservas[0]["precio_total"] == 2000000

def test_crear_reservas_recurrentes(monkeypatch):
    reservas_preparadas = [
        {"id": None},
        {"id": None},
        {"id": None},
        {"id": None},
    ]

    reservas_creadas = [
        {"id": 1},
        {"id": 2},
        {"id": 3},
        {"id": 4},
    ]

    monkeypatch.setattr(
        "services.reservas_recurrentes.construir_reservas",
        lambda datos: reservas_preparadas,
    )

    monkeypatch.setattr(
        "services.reservas_recurrentes."
        "repo_reservas_recurrentes.crear_serie",
        lambda reservas: reservas_creadas,
    )

    resultado = crear_reservas_recurrentes({})

    assert resultado == reservas_creadas
    assert len(resultado) == 4