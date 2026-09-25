from datetime import datetime

from repositories import bloqueos as repo
from validators.comunes import (
    campo_texto_no_vacio,
    campo_entero_positivo,
    entero,
    leer_paginacion,
    validar_cuerpo,
    validar_parametros_permitidos,
    error_campo,
)

PARAMS_LISTADO = {'id_cancha', 'fecha', '_limit', '_offset'}
CAMPOS_CREATE = {'id_cancha', 'fecha', 'hora_inicio', 'hora_fin', 'motivo'}

def validar_formato_fecha(fecha):
    try:
        return datetime.strptime(fecha, '%Y-%m-%d').date()
    except ValueError:
        return None

def validar_formato_horario(horario):
    try:
        return datetime.strptime(horario, '%H:%M:%S').time()
    except ValueError:
        return None

def campo_fecha(body, nombre, requerido, actual=None):
    if nombre not in body:
        if requerido:
            raise error_campo(nombre, 'es obligatorio')
        return actual
    valor = body[nombre]
    if not isinstance(valor, str):
        raise error_campo(nombre, 'debe ser un texto')
    limpio = valor.strip()
    if not limpio:
        raise error_campo(nombre, 'no puede quedar vacío')
    fecha_validada = validar_formato_fecha(limpio)
    if fecha_validada is None:
        raise error_campo(nombre, 'debe ser fecha valida (YYYY-MM-DD)')
    return fecha_validada

def campo_horario(body, nombre, requerido, actual=None):
    if nombre not in body:
        if requerido:
            raise error_campo(nombre, 'es obligatorio')
        return actual
    valor = body[nombre]
    if not isinstance (valor, str):
        raise error_campo(nombre, 'debe ser texto')
    limpio = valor.strip()
    if not limpio:
        raise error_campo(nombre, 'no puede quedar vacío')
    horario_valido = validar_formato_horario(limpio)
    if horario_valido is None:
        raise error_campo(nombre, 'debe ser horario valido (HH:MM:SS)')
    return horario_valido

def _validar_rango_horario(horario_inicial, horario_final):
    if horario_final < horario_inicial:
        raise error_campo('hora_fin', 'la hora de finalizacion no puede ocurrir antes que la hora de inicio')

def validar_filtros_listado(args):
    validar_parametros_permitidos(args, PARAMS_LISTADO)
    limit, offset = leer_paginacion(args)

    filtros={
        'id_cancha' : None,
        'fecha' : None,
    }
    if 'id_cancha' in args:
        filtros['id_cancha'] = entero(args['id_cancha'], 'id_cancha', 1)
    if 'fecha' in args:
        filtros['fecha'] = validar_formato_fecha(args['fecha'])

    return filtros, limit, offset

def validar_creacion(body):
    validar_cuerpo(body, CAMPOS_CREATE)

    id_cancha = campo_entero_positivo(body, 'id_cancha', requerido=True)
    fecha = campo_fecha(body, 'fecha', requerido=True)
    hora_inicio = campo_horario(body, 'hora_inicio', requerido=True)
    hora_fin = campo_horario(body, 'hora_fin', requerido=True)
    motivo = campo_texto_no_vacio(body, 'motivo', requerido=True)

    _validar_rango_horario(hora_inicio, hora_fin)

    return{
        'id_cancha': id_cancha,
        'fecha': fecha,
        'hora_inicio': hora_inicio,
        'hora_fin': hora_fin,
        'motivo': motivo,
        }