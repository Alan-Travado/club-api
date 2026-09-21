



CREATE TABLE IF NOT EXISTS deportes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS canchas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_deporte INT NOT NULL,
    precio_hora INT NOT NULL,
    techada BOOLEAN NOT NULL DEFAULT FALSE,
    activa BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT chk_cancha_precio CHECK (precio_hora > 0),
    CONSTRAINT fk_cancha_deporte FOREIGN KEY (id_deporte) REFERENCES deportes(id)
);

CREATE TABLE IF NOT EXISTS socios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_socio INT NOT NULL,
    id_cancha INT NOT NULL,
    fecha_hora_inicio DATETIME(6) NOT NULL,
    fecha_hora_fin DATETIME(6) NOT NULL,
    estado ENUM('confirmada', 'cancelada', 'finalizada') NOT NULL DEFAULT 'confirmada',
    precio_hora INT NOT NULL,
    precio_total INT NOT NULL,
    CONSTRAINT chk_reserva_intervalo CHECK (fecha_hora_inicio < fecha_hora_fin),
    CONSTRAINT chk_reserva_precios CHECK (precio_hora > 0 AND precio_total > 0),
    CONSTRAINT fk_reserva_socio FOREIGN KEY (id_socio) REFERENCES socios(id),
    CONSTRAINT fk_reserva_cancha FOREIGN KEY (id_cancha) REFERENCES canchas(id),
    INDEX idx_reserva_cancha (id_cancha, fecha_hora_inicio, fecha_hora_fin),
    INDEX idx_reserva_socio (id_socio, fecha_hora_inicio, fecha_hora_fin)
);

CREATE TABLE IF NOT EXISTS bloqueos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cancha INT NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    motivo VARCHAR(255) NOT NULL,
    CONSTRAINT chk_bloqueo_horas CHECK (hora_inicio < hora_fin),
    CONSTRAINT fk_bloqueo_cancha FOREIGN KEY (id_cancha) REFERENCES canchas(id),
    INDEX idx_bloqueo_cancha (id_cancha, fecha)
);

INSERT IGNORE INTO deportes (id, nombre) VALUES
    (1, 'Fútbol'),
    (2, 'Tenis'),
    (3, 'Pádel');