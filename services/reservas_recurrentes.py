from datetime import timedelta

def generar_serie(inicio, fin, cantidad_semanas):
    reservas = []

    for semana in range(cantidad_semanas):
        desplazamiento = timedelta(weeks=semana)
        reservas.append({
            "fecha_hora_inicio": inicio + desplazamiento,
            "fecha_hora_fin": fin + desplazamiento
        })
    return reservas
