from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from db import obtener_conexion


def main():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("UPDATE usuarios SET rol = 'tecnico' WHERE rol = 'gestor'")
        cursor.execute(
            """
            ALTER TABLE usuarios
            MODIFY COLUMN rol ENUM('cliente', 'tecnico', 'gestor', 'administrador') NOT NULL DEFAULT 'cliente'
            """
        )
        conexion.commit()
        print("Migración de rol técnico aplicada correctamente.")
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":
    main()
