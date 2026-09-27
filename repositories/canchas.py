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


def crear(datos):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO canchas (nombre, id_deporte, precio_hora, techada, activa) "
            "VALUES (%s, %s, %s, %s, %s)",
            (
                datos["nombre"],
                datos["id_deporte"],
                datos["precio_hora"],
                datos["techada"],
                datos["activa"],
            ),
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
    finally:
        conn.close()
    return obtener_por_id(nuevo_id)

def contar_reservas(id_cancha):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT COUNT(*) AS total FROM reservas WHERE id_cancha = %s",
            (id_cancha,),
        )
        total = cursor.fetchone()["total"]
    finally:
        conn.close()
    return total

def actualizar(id_cancha, datos):
    columnas = []
    valores = []

    for campo, valor in datos.items():
        columnas.append(f"{campo} = %s")
        valores.append(valor)

    valores.append(id_cancha)

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE canchas SET {', '.join(columnas)} WHERE id = %s",
            valores,
        )
        conn.commit()
    finally:
        conn.close()

    return obtener_por_id(id_cancha)


def eliminar(id_cancha):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM canchas WHERE id = %s",
            (id_cancha,),
        )
        conn.commit()
    finally:
        conn.close()

def listar_disponibles(filtros, inicio, fin, limit, offset):
    condiciones = ["c.activa = TRUE"]
    valores = []

    if filtros["id_deporte"] is not None:
        condiciones.append("c.id_deporte = %s")
        valores.append(filtros["id_deporte"])

    if filtros["techada"] is not None:
        condiciones.append("c.techada = %s")
        valores.append(filtros["techada"])

    condiciones.append(
        """
        NOT EXISTS (
            SELECT 1
            FROM reservas r
            WHERE r.id_cancha = c.id
              AND r.estado = 'confirmada'
              AND r.fecha_hora_inicio < %s
              AND r.fecha_hora_fin > %s
        )
        """
    )
    valores.extend([fin, inicio])

    condiciones.append(
        """
        NOT EXISTS (
            SELECT 1
            FROM bloqueos b
            WHERE b.id_cancha = c.id
              AND b.fecha = DATE(%s)
              AND b.hora_inicio < TIME(%s)
              AND b.hora_fin > TIME(%s)
        )
        """
    )
    valores.extend([inicio, fin, inicio])

    where = "WHERE " + " AND ".join(condiciones)

    conn = get_connection()

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            f"SELECT COUNT(*) AS total FROM canchas c {where}",
            valores,
        )
        total = cursor.fetchone()["total"]

        cursor.execute(
            f"""
            SELECT
                c.id,
                c.nombre,
                c.id_deporte,
                c.precio_hora,
                c.techada,
                c.activa
            FROM canchas c
            {where}
            ORDER BY c.id ASC
            LIMIT %s OFFSET %s
            """,
            valores + [limit, offset],
        )

        filas = [_normalizar(fila) for fila in cursor.fetchall()]

    finally:
        conn.close()

    return filas, total