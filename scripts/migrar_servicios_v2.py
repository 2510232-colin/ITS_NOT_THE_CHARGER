from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from db import obtener_conexion


COLUMNAS_OBJETIVO = {
    "categoria": "ALTER TABLE servicios ADD COLUMN categoria VARCHAR(120) NOT NULL DEFAULT 'General' AFTER id",
    "tipo_precio": "ALTER TABLE servicios ADD COLUMN tipo_precio ENUM('fijo', 'desde', 'rango', 'recargo') NOT NULL DEFAULT 'fijo' AFTER descripcion",
    "precio_min": "ALTER TABLE servicios ADD COLUMN precio_min DECIMAL(10,2) NULL AFTER precio",
    "precio_max": "ALTER TABLE servicios ADD COLUMN precio_max DECIMAL(10,2) NULL AFTER precio_min",
    "requiere_diagnostico": "ALTER TABLE servicios ADD COLUMN requiere_diagnostico TINYINT(1) NOT NULL DEFAULT 0 AFTER precio_max",
    "modalidad": "ALTER TABLE servicios ADD COLUMN modalidad ENUM('sucursal', 'domicilio', 'remoto', 'mixto') NOT NULL DEFAULT 'sucursal' AFTER requiere_diagnostico",
    "tiempo_estimado": "ALTER TABLE servicios ADD COLUMN tiempo_estimado VARCHAR(80) NULL AFTER modalidad",
}


def main():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("SHOW COLUMNS FROM servicios")
        existentes = {fila["Field"] for fila in cursor.fetchall()}

        for columna, sentencia in COLUMNAS_OBJETIVO.items():
            if columna not in existentes:
                cursor.execute(sentencia)

        conexion.commit()
        print("Migración servicios v2 aplicada correctamente.")
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":
    main()
