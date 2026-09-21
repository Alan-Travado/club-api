from db import get_connection


def listar():
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre FROM deportes ORDER BY id")
        return cursor.fetchall()
    finally:
        conn.close()
