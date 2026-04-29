from pathlib import Path
import sys

from werkzeug.security import generate_password_hash

sys.path.append(str(Path(__file__).resolve().parent.parent))

from db import obtener_conexion


def ejecutar_esquema(cursor, ruta_sql):
    contenido = Path(ruta_sql).read_text(encoding="utf-8")
    sentencias = [parte.strip() for parte in contenido.split(";") if parte.strip()]

    for sentencia in sentencias:
        cursor.execute(sentencia)


def insertar_admin(cursor):
    correo = "2510232@cesba-queretaro.edu.mx"
    contrasena_hash = generate_password_hash("Holaleo321.")
    nombres = "Leonardo Miguel"
    apellidos = "Colin Becerra"
    numero = "4424571413"

    cursor.execute(
        """
        INSERT INTO usuarios (correo, contrasena_hash, nombres, apellidos, numero, rol, activo)
        VALUES (%s, %s, %s, %s, %s, 'administrador', 1)
        ON DUPLICATE KEY UPDATE
            contrasena_hash = VALUES(contrasena_hash),
            nombres = VALUES(nombres),
            apellidos = VALUES(apellidos),
            numero = VALUES(numero),
            rol = VALUES(rol),
            activo = VALUES(activo)
        """,
        (correo, contrasena_hash, nombres, apellidos, numero),
    )


def insertar_contenido_inicial(cursor):
    cursor.execute(
        """
        INSERT INTO contenido_sitio (id, titulo_hero, subtitulo_hero, mensaje_promocional)
        VALUES (1, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            titulo_hero = VALUES(titulo_hero),
            subtitulo_hero = VALUES(subtitulo_hero),
            mensaje_promocional = VALUES(mensaje_promocional)
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
        ruta_esquema = Path(__file__).resolve().parent.parent / "sql" / "esquema.sql"
        ejecutar_esquema(cursor, ruta_esquema)
        insertar_admin(cursor)
        insertar_contenido_inicial(cursor)
        conexion.commit()
        print("Base de datos inicializada correctamente con administrador precargado.")
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":
    main()
