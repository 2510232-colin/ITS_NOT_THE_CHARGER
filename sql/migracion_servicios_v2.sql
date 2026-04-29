ALTER TABLE servicios
    ADD COLUMN IF NOT EXISTS categoria VARCHAR(120) NOT NULL DEFAULT 'General',
    ADD COLUMN IF NOT EXISTS tipo_precio ENUM('fijo', 'desde', 'rango', 'recargo') NOT NULL DEFAULT 'fijo',
    ADD COLUMN IF NOT EXISTS precio_min DECIMAL(10,2) NULL,
    ADD COLUMN IF NOT EXISTS precio_max DECIMAL(10,2) NULL,
    ADD COLUMN IF NOT EXISTS requiere_diagnostico TINYINT(1) NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS modalidad ENUM('sucursal', 'domicilio', 'remoto', 'mixto') NOT NULL DEFAULT 'sucursal',
    ADD COLUMN IF NOT EXISTS tiempo_estimado VARCHAR(80) NULL;
