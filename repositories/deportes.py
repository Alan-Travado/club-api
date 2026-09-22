from db import get_connection


def listar():
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre FROM deportes ORDER BY id")
        return cursor.fetchall()
    finally:
        conn.close()


def existe(id_deporte):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM deportes WHERE id = %s", (id_deporte,))
        return cursor.fetchone() is not None
    finally:
        conn.close()
