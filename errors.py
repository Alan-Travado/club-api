from flask import jsonify
from werkzeug.exceptions import HTTPException


class ApiError(Exception):
    def __init__(
            self, 
            status, 
            code, 
            message, 
            description, 
            conflictos=None
    ):
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message
        self.description = description
        self.conflictos = conflictos


def error_response(status, code, message, description, level="error", conflictos=None):
    body = {
        "errors": [
            {
                "code": code,
                "message": message,
                "level": level,
                "description": description,
            }
        ]
    }
    if conflictos is not None:
        body["conflictos"] = conflictos
    return jsonify(body), status


def registrar_manejadores(app):
    @app.errorhandler(ApiError)
    def manejar_api_error(e):
        return error_response(e.status, e.code, e.message, e.description, conflictos=e.conflictos)

    @app.errorhandler(HTTPException)
    def manejar_http(e):
        return error_response(e.code, "ERROR_HTTP", e.name, e.description)

    @app.errorhandler(Exception)
    def manejar_inesperado(e):
        app.logger.exception(e)
        return error_response(
            500,
            "ERROR_INTERNO",
            "Error interno del servidor",
            "Ocurrió un error inesperado",
        )
