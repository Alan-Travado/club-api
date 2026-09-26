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

    validador_reserva_nueva(
        2,
        1,
        inicio,
        fin,
    )