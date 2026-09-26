from db import get_connection
from validators import comunes

def existe_cancha(id_cancha):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM canchas WHERE id = %s LIMIT 1', (id_cancha,))
        fila = cursor.fetchone()
    finally:
        conn.close()
    return fila is not None

def hay_superposicion_con_bloqueo(filtros):
    condiciones = []
    valores = []
 
    if filtros.get('id_cancha') is not None:
        condiciones.append('id_cancha = %s')
        valores.append(filtros['id_cancha'])
    if filtros.get('fecha') is not None:
        condiciones.append('fecha = %s')
        valores.append(filtros['fecha'])
    if filtros.get('hora_inicio') is not None and filtros.get('hora_fin') is not None:
        condiciones.append('hora_inicio < %s')
        valores.append(filtros['hora_fin'])
        condiciones.append('hora_fin > %s')
        valores.append(filtros['hora_inicio'])
 
    where = ''
    if condiciones:
        where = 'WHERE ' + ' AND '.join(condiciones)
 
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f'SELECT 1 FROM bloqueos {where} LIMIT 1', tuple(valores))
        fila = cursor.fetchone()
    finally:
        conn.close()
 
    return fila is not None

def crear(datos):
    conn=get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            'INSERT INTO bloqueos (id_cancha, fecha, hora_inicio, hora_fin, motivo) VALUES (%s, %s, %s, %s, %s)',
            (
                datos['id_cancha'],
                datos['fecha'],
                datos['hora_inicio'],
                datos['hora_fin'],
                datos['motivo'],
            ),
        )
        conn.commit()
        nuevo_bloqueo = cursor.lastrowid

    finally:
        conn.close()
    return nuevo_bloqueo

def listar(filtros, limit, offset):
    condiciones = []
    valores = []

    if filtros.get('id_cancha') is not None:
        condiciones.append('id_cancha = %s')
        valores.append(filtros['id_cancha'])
    if filtros.get('fecha') is not None:
        condiciones.append('fecha = %s')
        valores.append(filtros['fecha'])

    where = ''
    if condiciones:
        where = 'WHERE ' + ' AND '.join(condiciones)

    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f'SELECT COUNT(*) AS total FROM bloqueos {where}', tuple(valores),)
        total = cursor.fetchone()['total']

        parametros = list(valores) + [limit, offset]
        cursor.execute(f'SELECT * FROM bloqueos {where} ORDER BY id ASC LIMIT %s OFFSET %s', tuple(parametros),)
        filas = cursor.fetchall()
        filas = [comunes.fechas_a_texto(fila) for fila in filas]

    finally:
        conn.close()
 
    return filas, total

def eliminar(id_bloqueo):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('DELETE FROM bloqueos WHERE id = %s', (id_bloqueo,))
        conn.commit()
        fila_afectada = cursor.rowcount
    finally:
        conn.close()
    return fila_afectada
 