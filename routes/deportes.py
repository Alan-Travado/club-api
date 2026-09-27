from flask import Blueprint, jsonify, request
from services import deportes as service
from validators.comunes import validar_sin_parametros

bp = Blueprint("deportes", __name__)


@bp.get("/deportes")
def listar_deportes():
    validar_sin_parametros(request.args)

    deportes = service.listar_deportes()
    if not deportes:
        return "", 204
    return jsonify({"deportes": deportes}), 200
