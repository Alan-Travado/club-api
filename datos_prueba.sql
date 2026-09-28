SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

USE club_deportivo;

INSERT INTO canchas (nombre, id_deporte, precio_hora, techada, activa) VALUES
    ('Cancha 1 - Fútbol 5', 1, 1000000, FALSE, TRUE),
    ('Cancha 2 - Fútbol 7', 1, 1500000, FALSE, TRUE),
    ('Cancha 3 - Tenis', 2, 800000, FALSE, TRUE),
    ('Cancha 4 - Pádel', 3, 1200000, TRUE, TRUE),
    ('Cancha 5 - Pádel', 3, 1200000, TRUE, FALSE);

INSERT INTO socios (nombre, email, activo) VALUES
    ('Juan Pérez', 'juan.perez@example.com', TRUE),
    ('María Gómez', 'maria.gomez@example.com', TRUE),
    ('Carlos López', 'carlos.lopez@example.com', FALSE);

INSERT INTO reservas (
    id_socio, id_cancha, fecha_hora_inicio, fecha_hora_fin,
    estado, precio_hora, precio_total
) VALUES
    (1, 1, '2030-10-15 18:00:00.000000', '2030-10-15 20:00:00.000000', 'confirmada', 1000000, 2000000),
    (2, 3, '2020-09-01 10:00:00.000000', '2020-09-01 12:00:00.000000', 'confirmada', 800000, 1600000),
    (1, 4, '2030-11-01 09:00:00.000000', '2030-11-01 10:00:00.000000', 'cancelada', 1200000, 1200000),
    (2, 1, '2020-08-10 15:00:00.000000', '2020-08-10 17:00:00.000000', 'finalizada', 1000000, 2000000);