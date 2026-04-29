from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from db import obtener_conexion


def main():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ticket_mensajes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_ticket INT NOT NULL,
                id_usuario INT NOT NULL,
                mensaje TEXT NOT NULL,
                fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_ticket) REFERENCES tickets(id),
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
            )
            """
        )
        conexion.commit()
        print("Migración ticket_mensajes v1 aplicada correctamente.")
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":
    main()
