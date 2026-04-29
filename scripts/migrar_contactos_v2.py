from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from db import obtener_conexion


def main():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("SHOW COLUMNS FROM contactos")
        columnas = {fila["Field"] for fila in cursor.fetchall()}

        if "atendido" not in columnas:
            cursor.execute("ALTER TABLE contactos ADD COLUMN atendido TINYINT(1) NOT NULL DEFAULT 0 AFTER mensaje")
            print("Columna atendido agregada en contactos.")
        else:
            print("La tabla contactos ya contiene la columna atendido.")

        conexion.commit()
        print("Migración contactos v2 aplicada correctamente.")
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":
    main()
