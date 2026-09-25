from db import get_connection


def existe_superposicion_en_cancha(id_cancha, inicio, fin, excluir_id=None):
    query = (
        "SELECT 1 FROM reservas "
        "WHERE id_cancha = %s AND estado = 'confirmada' "
        "AND fecha_hora_inicio < %s AND fecha_hora_fin > %s"
    )
    valores = [id_cancha, fin, inicio]
    if excluir_id is not None:
        query += " AND id != %s"
        valores.append(excluir_id)
    query += " LIMIT 1"

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, valores)
        return cursor.fetchone() is not None
    finally:
        conn.close()


def existe_superposicion_en_socio(id_socio, inicio, fin, excluir_id=None):
    query = (
        "SELECT 1 FROM reservas "
        "WHERE id_socio = %s AND estado = 'confirmada' "
        "AND fecha_hora_inicio < %s AND fecha_hora_fin > %s"
    )
    valores = [id_socio, fin, inicio]
    if excluir_id is not None:
        query += " AND id != %s"
        valores.append(excluir_id)
    query += " LIMIT 1"

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, valores)
        return cursor.fetchone() is not None
    finally:
        conn.close()
