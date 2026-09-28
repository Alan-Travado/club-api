from db import get_connection
from reglas_horario import a_naive

def crear_serie(reservas):
    conn = get_connection()

    try:
        cursor = conn.cursor()
        creadas = []

        query = """
        INSERT INTO reservas (id_cancha, id_socio, fecha_hora_inicio, fecha_hora_fin, estado, precio_hora, precio_total)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        for reserva in reservas:
            valores = (
                reserva["id_cancha"],
                reserva["id_socio"],
                a_naive(reserva["fecha_hora_inicio"]),
                a_naive(reserva["fecha_hora_fin"]),
                reserva["estado"],
                reserva.get("precio_hora"),
                reserva.get("precio_total"),
            )

            cursor.execute(query, valores)

            creada = reserva.copy()
            creada["id"] = cursor.lastrowid
            creadas.append(creada)
        
        conn.commit()
        return creadas

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()