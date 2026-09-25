from datetime import datetime, timedelta, timezone

import pytest

from repositories.reservas_recurrentes import crear_serie


class CursorFalso:
    def __init__(self, fallar_en=None):
        self.ejecuciones = 0
        self.lastrowid = 0
        self.fallar_en = fallar_en

    def execute(self, query, valores):
        self.ejecuciones += 1

        if self.ejecuciones == self.fallar_en:
            raise RuntimeError("Error simulado")

        self.lastrowid = self.ejecuciones


class ConexionFalsa:
    def __init__(self, fallar_en=None):
        self.cursor_falso = CursorFalso(fallar_en)
        self.commit_hecho = False
        self.rollback_hecho = False
        self.cerrada = False

    def cursor(self):
        return self.cursor_falso

    def commit(self):
        self.commit_hecho = True

    def rollback(self):
        self.rollback_hecho = True

    def close(self):
        self.cerrada = True

def test_crear_serie_hace_commit(monkeypatch):
    zona = timezone(timedelta(hours=-3))

    reservas = [
        {
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

    conexion = ConexionFalsa()

    monkeypatch.setattr(
        "repositories.reservas_recurrentes.get_connection",
        lambda: conexion,
    )

    creadas = crear_serie(reservas)

    assert conexion.commit_hecho is True
    assert conexion.rollback_hecho is False
    assert conexion.cerrada is True
    assert creadas[0]["id"] == 1

def test_crear_serie_hace_rollback_si_falla(monkeypatch):
    zona = timezone(timedelta(hours=-3))

    reservas = []

    for semana in range(3):
        inicio = datetime(2026, 10, 15, 18, 0, tzinfo=zona) + timedelta(weeks=semana)

        reservas.append({
            "id_socio": 1,
            "id_cancha": 2,
            "fecha_hora_inicio": inicio,
            "fecha_hora_fin": inicio + timedelta(hours=2),
            "estado": "confirmada",
            "precio_hora": 1000000,
            "precio_total": 2000000,
        })

    conexion = ConexionFalsa(fallar_en=2)

    monkeypatch.setattr(
        "repositories.reservas_recurrentes.get_connection",
        lambda: conexion,
    )

    with pytest.raises(RuntimeError):
        crear_serie(reservas)

    assert conexion.commit_hecho is False
    assert conexion.rollback_hecho is True
    assert conexion.cerrada is True