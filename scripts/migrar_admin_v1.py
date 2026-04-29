from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from db import obtener_conexion


def asegurar_tabla_pedidos(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pedidos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            folio VARCHAR(30) NOT NULL UNIQUE,
            id_usuario INT NOT NULL,
            total DECIMAL(10,2) NOT NULL DEFAULT 0,
            estado ENUM('Pendiente', 'En preparación', 'Listo para recoger', 'Entregado') NOT NULL DEFAULT 'Pendiente',
            fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        )
        """
    )


def asegurar_tabla_contenido(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS contenido_sitio (
            id INT PRIMARY KEY,
            titulo_hero VARCHAR(180) NOT NULL,
            subtitulo_hero TEXT NOT NULL,
            mensaje_promocional VARCHAR(220) NOT NULL,
            fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
    )


def asegurar_contenido_inicial(cursor):
    cursor.execute(
        """
        INSERT INTO contenido_sitio (id, titulo_hero, subtitulo_hero, mensaje_promocional)
        VALUES (1, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            titulo_hero = titulo_hero
        """,
        (
            "Servicio técnico premium para tu equipo",
            "Atención ordenada, rápida y con estilo tecnológico.",
            "Promociones semanales disponibles en sucursal.",
        ),
    )


def main():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        asegurar_tabla_pedidos(cursor)
        asegurar_tabla_contenido(cursor)
        asegurar_contenido_inicial(cursor)
        conexion.commit()
        print("Migración admin v1 aplicada correctamente.")
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":
    main()
