from flask import Blueprint, jsonify
from services import canchas as service

bp = Blueprint("canchas", __name__)


@bp.get("/canchas/<int:id_cancha>")
def obtener_cancha(id_cancha):
    return jsonify(service.obtener_cancha(id_cancha)), 200
