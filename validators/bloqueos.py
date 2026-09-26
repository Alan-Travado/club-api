from repositories import bloqueos as repo
from validators.comunes import (
    campo_texto_no_vacio,
    campo_entero_positivo,
    entero,
    leer_paginacion,
    validar_cuerpo,
    validar_parametros_permitidos,
    error_campo,
    parametro_fecha,
    combinar_fecha_hora,
    campo_fecha,
    campo_hora,
)
import reglas_horario

PARAMS_LISTADO = {'id_cancha', 'fecha', '_limit', '_offset'}
CAMPOS_CREATE = {'id_cancha', 'fecha', 'hora_inicio', 'hora_fin', 'motivo'}

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
        filtros['fecha'] = parametro_fecha(args['fecha'])

    return filtros, limit, offset

def validar_creacion(body):
    validar_cuerpo(body, CAMPOS_CREATE)

    id_cancha = campo_entero_positivo(body, 'id_cancha', requerido=True)
    fecha = campo_fecha(body, 'fecha', requerido=True)
    hora_inicio = campo_hora(body, 'hora_inicio', requerido=True)
    hora_fin = campo_hora(body, 'hora_fin', requerido=True)
    motivo = campo_texto_no_vacio(body, 'motivo', requerido=True)

    fecha_inicio = combinar_fecha_hora(fecha, hora_inicio)
    fecha_fin = combinar_fecha_hora(fecha, hora_fin)

    _validar_rango_horario(hora_inicio, hora_fin)
    reglas_horario.validar_intervalo(fecha_inicio, fecha_fin, limite_duracion=False)

    return{
        'id_cancha': id_cancha,
        'fecha': fecha,
        'hora_inicio': hora_inicio,
        'hora_fin': hora_fin,
        'motivo': motivo,
        }