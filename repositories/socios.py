from db import get_connection

COLUMNAS = "id, nombre, email, activo"


def _normalizar(fila):
    fila["activo"] = bool(fila["activo"])
    return fila


def _escapar_like(texto):
    return texto.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def obtener_por_id(id_socio):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            f"SELECT {COLUMNAS} FROM socios WHERE id = %s",
            (id_socio,),
        )
        fila = cursor.fetchone()
    finally:
        conn.close()
    return _normalizar(fila) if fila else None


def obtener_por_email(email, excluir_id=None):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        if excluir_id is None:
            cursor.execute(
                f"SELECT {COLUMNAS} FROM socios WHERE email = %s",
                (email,),
            )
        else:
            cursor.execute(
                f"SELECT {COLUMNAS} FROM socios WHERE email = %s AND id != %s",
                (email, excluir_id),
            )
        fila = cursor.fetchone()
    finally:
        conn.close()
    return _normalizar(fila) if fila else None


def listar(filtros, limit, offset):
    condiciones = []
    valores = []

    if filtros["nombre"] is not None:
        condiciones.append("nombre LIKE %s")
        valores.append(f"%{_escapar_like(filtros['nombre'])}%")
    if filtros["activo"] is not None:
        condiciones.append("activo = %s")
        valores.append(filtros["activo"])

    where = ""
    if condiciones:
        where = "WHERE " + " AND ".join(condiciones)

    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT COUNT(*) AS total FROM socios {where}", valores)
        total = cursor.fetchone()["total"]

        cursor.execute(
            f"SELECT {COLUMNAS} FROM socios {where} "
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
            "INSERT INTO socios (nombre, email, activo) VALUES (%s, %s, %s)",
            (datos["nombre"], datos["email"], datos["activo"]),
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
    finally:
        conn.close()
    return obtener_por_id(nuevo_id)


def actualizar(id_socio, datos):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE socios SET nombre = %s, email = %s, activo = %s WHERE id = %s",
            (datos["nombre"], datos["email"], datos["activo"], id_socio),
        )
        conn.commit()
    finally:
        conn.close()
    return obtener_por_id(id_socio)
