from db import get_connection
from validators import comunes
from reglas_horario import a_naive

COLUMNAS = (
    "id, id_socio, id_cancha, fecha_hora_inicio, fecha_hora_fin, "
    "estado, precio_hora, precio_total"
)


def formatear(fila):
    fila = dict(fila)
    fila["fecha_hora_inicio"] = _fmt(fila["fecha_hora_inicio"])
    fila["fecha_hora_fin"] = _fmt(fila["fecha_hora_fin"])
    return fila


def _fmt(valor):
    return valor.strftime("%Y-%m-%dT%H:%M:%S.%f") + "-03:00"


def obtener_por_id(id_reserva):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT {COLUMNAS} FROM reservas WHERE id = %s", (id_reserva,))
        return cursor.fetchone()
    finally:
        conn.close()

def crear(datos):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO reservas (
                id_socio,
                id_cancha,
                fecha_hora_inicio,
                fecha_hora_fin,
                estado,
                precio_hora,
                precio_total
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                datos["id_socio"],
                datos["id_cancha"],
                a_naive(datos["fecha_hora_inicio"]),
                a_naive(datos["fecha_hora_fin"]),
                datos["estado"],
                datos["precio_hora"],
                datos["precio_total"],
            ),
        )

        nuevo_id = cursor.lastrowid
        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    return formatear(obtener_por_id(nuevo_id))

def listar(filtros, limit, offset):
    condiciones = []
    valores = []
    if filtros["id_cancha"] is not None:
        condiciones.append("id_cancha = %s")
        valores.append(filtros["id_cancha"])
    if filtros["id_socio"] is not None:
        condiciones.append("id_socio = %s")
        valores.append(filtros["id_socio"])
    if filtros["estado"] is not None:
        condiciones.append("estado = %s")
        valores.append(filtros["estado"])
    if filtros["fecha_desde"] is not None:
        condiciones.append("DATE(fecha_hora_inicio) >= %s")
        valores.append(filtros["fecha_desde"])
    if filtros["fecha_hasta"] is not None:
        condiciones.append("DATE(fecha_hora_inicio) <= %s")
        valores.append(filtros["fecha_hasta"])

    where = ""
    if condiciones:
        where = "WHERE " + " AND ".join(condiciones)

    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT COUNT(*) AS total FROM reservas {where}", valores)
        total = cursor.fetchone()["total"]
        cursor.execute(
            f"SELECT {COLUMNAS} FROM reservas {where} "
            "ORDER BY id ASC LIMIT %s OFFSET %s",
            valores + [limit, offset],
        )
        filas = [formatear(f) for f in cursor.fetchall()]
    finally:
        conn.close()
    return filas, total


def actualizar_estado(id_reserva, estado_nuevo, estado_anterior):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE reservas SET estado = %s WHERE id = %s AND estado = %s",
            (estado_nuevo, id_reserva, estado_anterior),
        )
        conn.commit()
        return cursor.rowcount == 1
    finally:
        conn.close()


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


def existe_superposicion_en_bloqueo(id_cancha, fecha, inicio, fin):
    valores = (id_cancha, fecha, comunes.hora_a_time(fin), comunes.hora_a_time(inicio))

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT 1 FROM bloqueos WHERE id_cancha = %s
            AND fecha = %s AND hora_inicio < %s AND hora_fin > %s LIMIT 1""",
            valores,
        )
        fila = cursor.fetchone()
    finally:
        conn.close()
    return fila is not None
