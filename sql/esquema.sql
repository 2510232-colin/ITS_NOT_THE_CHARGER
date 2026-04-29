CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    correo VARCHAR(120) NOT NULL UNIQUE,
    contrasena_hash VARCHAR(255) NOT NULL,
    nombres VARCHAR(60) NOT NULL,
    apellidos VARCHAR(60) NOT NULL,
    numero VARCHAR(15) NOT NULL,
    rol ENUM('cliente', 'tecnico', 'gestor', 'administrador') NOT NULL DEFAULT 'cliente',
    activo TINYINT(1) NOT NULL DEFAULT 1,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS servicios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    categoria VARCHAR(120) NOT NULL DEFAULT 'General',
    nombre VARCHAR(120) NOT NULL,
    descripcion TEXT,
    tipo_precio ENUM('fijo', 'desde', 'rango', 'recargo') NOT NULL DEFAULT 'fijo',
    precio DECIMAL(10,2) NOT NULL DEFAULT 0,
    precio_min DECIMAL(10,2) NULL,
    precio_max DECIMAL(10,2) NULL,
    requiere_diagnostico TINYINT(1) NOT NULL DEFAULT 0,
    modalidad ENUM('sucursal', 'domicilio', 'remoto', 'mixto') NOT NULL DEFAULT 'sucursal',
    tiempo_estimado VARCHAR(80) NULL,
    palabras_clave VARCHAR(500) NULL,
    destacado_inicio TINYINT(1) NOT NULL DEFAULT 0,
    orden_destacado INT NOT NULL DEFAULT 0,
    promocion_activa TINYINT(1) NOT NULL DEFAULT 0,
    promocion_texto VARCHAR(180) NULL,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL DEFAULT 0,
    stock INT NOT NULL DEFAULT 0,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    folio VARCHAR(30) NOT NULL UNIQUE,
    id_usuario INT NOT NULL,
    servicio_solicitado VARCHAR(140) NOT NULL,
    equipo VARCHAR(140) NOT NULL,
    descripcion TEXT NOT NULL,
    precio_estimado_referencial DECIMAL(10,2) NULL,
    detalle_precio_estimado VARCHAR(220) NULL,
    acepta_politica_domicilio TINYINT(1) NOT NULL DEFAULT 0,
    estado ENUM('Recibido', 'En revisión', 'En proceso', 'Listo para recoger', 'Entregado') NOT NULL DEFAULT 'Recibido',
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS contactos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    correo VARCHAR(120) NOT NULL,
    mensaje TEXT NOT NULL,
    atendido TINYINT(1) NOT NULL DEFAULT 0,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ticket_mensajes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_ticket INT NOT NULL,
    id_usuario INT NOT NULL,
    mensaje TEXT NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_ticket) REFERENCES tickets(id),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    folio VARCHAR(30) NOT NULL UNIQUE,
    id_usuario INT NOT NULL,
    total DECIMAL(10,2) NOT NULL DEFAULT 0,
    estado ENUM('Pendiente', 'En preparación', 'Listo para recoger', 'Entregado') NOT NULL DEFAULT 'Pendiente',
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS contenido_sitio (
    id INT PRIMARY KEY,
    titulo_hero VARCHAR(180) NOT NULL,
    subtitulo_hero TEXT NOT NULL,
    mensaje_promocional VARCHAR(220) NOT NULL,
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
