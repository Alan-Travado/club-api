from db import get_connection


def obtener_por_id(id_cancha):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, nombre, id_deporte, precio_hora, techada, activa "
            "FROM canchas WHERE id = %s",
            (id_cancha,),
        )
        fila = cursor.fetchone()
    finally:
        conn.close()
    if fila:
        fila["techada"] = bool(fila["techada"])
        fila["activa"] = bool(fila["activa"])
    return fila
