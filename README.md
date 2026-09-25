===========================================================
HORARIOS Y SUPERPOSICIONES ( miembro 2 finalizado)
Que se hizo y que se probó 
===========================================================

Branch: feature/horarios-superposiciones (sobre Develop)

------------------------------------------------------------
1) ARCHIVOS NUEVOS / MODIFICADOS
------------------------------------------------------------

- reglas_horario.py (NUEVO)
  Función principal: validar_intervalo(inicio, fin)
  Valida que un intervalo de reserva cumpla TODAS las reglas
  del enunciado:
    * fecha_hora_fin debe ser posterior a fecha_hora_inicio
    * debe comenzar y terminar en una hora en punto (sin
      minutos, segundos ni microsegundos)
    * no puede atravesar la medianoche
    * debe estar dentro del horario del club (08:00 a 23:00)
    * la duración debe ser de 1 a 3 horas completas
    * el inicio debe ser posterior al momento actual
  También define ZONA_CLUB (GMT-3 fijo, sin conversión de
  huso horario) y la función ahora(), que da la hora actual
  ya en esa zona, sin importar en qué huso esté configurado
  el servidor.

- validators/comunes.py (MODIFICADO)
  Se agregó el parseo (conversión de texto a datetime/date/
  hora) de los formatos que pide el swagger:
    * campo_fecha_hora(): para el formato ISO 8601 completo
      usado en el body de POST /reservas
      (YYYY-MM-DDTHH:MM:SS.ffffff-03:00)
    * parametro_fecha(): para el parámetro "fecha" (YYYY-MM-DD)
      usado en GET /canchas/disponibles
    * parametro_hora(): para "hora_inicio"/"hora_fin"
      (HH:00:00, solo horas en punto)
    * combinar_fecha_hora(): junta una fecha y una hora en un
      datetime único con la zona del club

- repositories/reservas.py (NUEVO)
  Funciones que consultan la base para detectar cruces de
  horario, comparando SIEMPRE contra reservas en estado
  'confirmada' (las canceladas o finalizadas no bloquean):
    * existe_superposicion_cancha(id_cancha, inicio, fin)
    * existe_superposicion_socio(id_socio, inicio, fin)
  Ambas usan la fórmula estándar de superposición de
  intervalos (inicio_existente < fin_nuevo AND
  fin_existente > inicio_nuevo), que cubre los casos que pide
  el enunciado: idénticos, contenidos, contenedores y
  parciales.

- services/disponibilidad.py (NUEVO)
  Junta las dos cosas de arriba en una sola función:
    validar_reserva_nueva(id_cancha, id_socio, inicio, fin)
  Primero valida el intervalo (reglas_horario), y si pasa,
  chequea superposición por cancha y por socio. Si algo
  falla, lanza un ApiError con el código y el status HTTP
  correctos (400 para horarios inválidos, 409 para
  superposiciones). Esta es la función que van a usar los
  endpoints POST /reservas y GET /canchas/disponibles.

------------------------------------------------------------
2) PPRUEBA
------------------------------------------------------------

PRUEBA A - Reglas de horario (validar_intervalo), 8 casos:
  1. Intervalo válido (2 horas, en punto, dentro de horario,
     futuro)                                  -> ACEPTADO ✔
  2. Antes de las 8:00                        -> RECHAZADO ✔
  3. Termina después de las 23:00             -> RECHAZADO ✔
  4. Duración de 4 horas (excede el máximo)   -> RECHAZADO ✔
  5. Intervalo de 0 horas (inicio = fin)      -> RECHAZADO ✔
  6. Hora no en punto (termina en :30)        -> RECHAZADO ✔
  7. Fecha en el pasado                       -> RECHAZADO ✔
  8. Fin antes que el inicio                  -> RECHAZADO ✔

  Resultado: los 8 casos dieron el resultado esperado.

PRUEBA B - Superposiciones (validar_reserva_nueva), con una
reserva real cargada en la base (cancha 1, socio 1, 18:00 a
20:00, confirmada), 5 casos:
  1. Otra reserva en la misma cancha que se solapa
     parcialmente (19-21)                     -> RECHAZADO ✔
     (409 CANCHA_NO_DISPONIBLE)
  2. Reserva consecutiva, sin cruce real (20-21)
                                               -> ACEPTADO ✔
  3. Mismo horario exacto, misma cancha       -> RECHAZADO ✔
     (409 CANCHA_NO_DISPONIBLE)
  4. Mismo socio (distinta cancha) con horario que se
     solapa                                   -> RECHAZADO ✔
     (409 SOCIO_NO_DISPONIBLE)
  5. Otra cancha, otro socio, mismo horario, sin conflicto
     real                                     -> ACEPTADO ✔

  Resultado: los 5 casos dieron el resultado esperado.



Detecto bien los casos que pide el enunciado  (superposición total, parcial, contenida,
contenedora, e idéntica) tanto paara la cancha como para el socio y tambien deja pasar los casos que si son validos ( reservas consecutivas)


------------------------------------------------------------
UN DETALLE TÉCNICO IMPORTANTE
------------------------------------------------------------

Todas las fechas se manejan como "datetime aware" en la zona
GMT-3 fija (reglas_horario.ZONA_CLUB), es decir que el programa va a manejar todas las fechas y horarios siempre como si estuviera en GMT-3, sin importar dónde este funcionando el servidor. Por ejemplo i se indica que algo ocurre a las 15:00, el programa entiende que son las 15:00 de GMT-3 y no va a convertir esa hora según la configuración de la computadora. Esto es asi porque el servidor podria estar configurado en otro huso horario, como UTC, o incluso estar dentro de un contenedor Docker con otra configuración. Para evitar problemas el programa tiene una zona horaria fija definida en reglas_horario. ZONA_CLUB, que es la que se usa siempre. Cuando dice que las fechas son "datetime aware", quiere decir simplemente que la fecha y hora llevan asociada información sobre su zona horaria, en este caso GMT-3. En resumen: no importa dónde esté la máquina ni qué hora tenga configurada; para este programa, la hora oficial siempre es GMT-3.

Al guardar en la base, MySQL no soporta guardar la zona
horaria (columna DATETIME), así que antes de un INSERT hay que
quitarle el tzinfo con reglas_horario.a_naive(dt). Esto ya lo
hace internamente validar_reserva_nueva antes de consultar
superposición pero quien guarde la reserva en el repository
también tiene que aplicarlo antes del INSERT.
