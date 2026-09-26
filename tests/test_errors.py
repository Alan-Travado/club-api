from flask import Flask
from errors import error_response

def test_error_response_con_conflictos():
    app = Flask(__name__)

    with app.app_context():
        respuesta, status = error_response(
            409,
            "RESERVAS_NO_DISPONIBLES",
            "Conflicto en la serie de reservas",
            "Una o más fechas no están disponibles",
            conflictos=[
                "2026-10-22",
                "2026-11-05",   
            ],
        )

        body = respuesta.get_json()

    assert status == 409

    assert body["conflictos"] == [
        "2026-10-22",
        "2026-11-05"
    ]

    assert body["errors"][0]["code"] == "RESERVAS_NO_DISPONIBLES"