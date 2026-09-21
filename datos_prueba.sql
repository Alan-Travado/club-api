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