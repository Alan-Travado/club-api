from flask import jsonify
from werkzeug.exceptions import HTTPException


class ApiError(Exception):
    def __init__(self, status, code, message, description):
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message
        self.description = description


def error_response(status, code, message, description, level="error"):
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
    return jsonify(body), status


def registrar_manejadores(app):
    @app.errorhandler(ApiError)
    def manejar_api_error(e):
        return error_response(e.status, e.code, e.message, e.description)

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
