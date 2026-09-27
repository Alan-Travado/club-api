import pytest

from errors import ApiError
from validators import socios as validador


def test_creacion_normaliza_email():
    datos = validador.validar_creacion({
        "nombre": "Ana",
        "email": "  ANA@EJEMPLO.COM  ",
    })

    assert datos["email"] == "ana@ejemplo.com"


def test_creacion_rechaza_email_invalido():
    with pytest.raises(ApiError) as error:
        validador.validar_creacion({
            "nombre": "Ana",
            "email": "ana@",
        })

    assert error.value.status == 400


def test_creacion_rechaza_email_faltante():
    with pytest.raises(ApiError) as error:
        validador.validar_creacion({
            "nombre": "Ana",
        })

    assert error.value.status == 400


def test_actualizacion_conserva_email_si_no_se_envia():
    actual = {
        "nombre": "Ana",
        "email": "ana@ejemplo.com",
        "activo": True,
    }

    datos = validador.validar_actualizacion(
        {"nombre": "Ana Maria"},
        actual,
    )

    assert datos["email"] == "ana@ejemplo.com"