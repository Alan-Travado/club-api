from flask import Blueprint, jsonify
from services import deportes as service

bp = Blueprint("deportes", __name__)


@bp.get("/deportes")
def listar_deportes():
    deportes = service.listar_deportes()
    if not deportes:
        return "", 204
    return jsonify({"deportes": deportes}), 200
