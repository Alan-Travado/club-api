from db import get_connection

COLUMNAS = "id, nombre, id_deporte, precio_hora, techada, activa"


def _normalizar(fila):
    fila["techada"] = bool(fila["techada"])
    fila["activa"] = bool(fila["activa"])
    return fila


def _escapar_like(texto):
    return texto.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def obtener_por_id(id_cancha):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            f"SELECT {COLUMNAS} FROM canchas WHERE id = %s",
            (id_cancha,),
        )
        fila = cursor.fetchone()
    finally:
        conn.close()
    return _normalizar(fila) if fila else None


def listar(filtros, limit, offset):
    condiciones = []
    valores = []

    if filtros["id_deporte"] is not None:
        condiciones.append("id_deporte = %s")
        valores.append(filtros["id_deporte"])
    if filtros["nombre"] is not None:
        condiciones.append("nombre LIKE %s")
        valores.append(f"%{_escapar_like(filtros['nombre'])}%")
    if filtros["techada"] is not None:
        condiciones.append("techada = %s")
        valores.append(filtros["techada"])
    if filtros["activa"] is not None:
        condiciones.append("activa = %s")
        valores.append(filtros["activa"])

    where = ""
    if condiciones:
        where = "WHERE " + " AND ".join(condiciones)

    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT COUNT(*) AS total FROM canchas {where}", valores)
        total = cursor.fetchone()["total"]

        cursor.execute(
            f"SELECT {COLUMNAS} FROM canchas {where} "
            "ORDER BY id ASC LIMIT %s OFFSET %s",
            valores + [limit, offset],
        )
        filas = [_normalizar(f) for f in cursor.fetchall()]
    finally:
        conn.close()
    return filas, total
