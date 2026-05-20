import os

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error


load_dotenv()


def obtener_configuracion_bd():
    configuracion = {
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "database": os.getenv("MYSQL_DATABASE", "techcare_db"),
        "autocommit": False,
    }

    ssl_mode = os.getenv("MYSQL_SSL_MODE", "DISABLED").strip().upper()
    if ssl_mode in {"REQUIRED", "VERIFY_CA", "VERIFY_IDENTITY"}:
        configuracion["ssl_disabled"] = False

        ssl_ca = os.getenv("MYSQL_SSL_CA", "").strip()
        if ssl_ca:
            configuracion["ssl_ca"] = ssl_ca

        if ssl_mode in {"VERIFY_CA", "VERIFY_IDENTITY"}:
            configuracion["ssl_verify_cert"] = True

        if ssl_mode == "VERIFY_IDENTITY":
            configuracion["ssl_verify_identity"] = True

    return configuracion


def obtener_conexion():
    configuracion = obtener_configuracion_bd()
    return mysql.connector.connect(**configuracion)


def ejecutar_consulta(sql, parametros=None, una_fila=False, varias_filas=False, confirmar=False):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql, parametros or ())

        if confirmar:
            conexion.commit()
            return cursor.lastrowid

        if una_fila:
            return cursor.fetchone()

        if varias_filas:
            return cursor.fetchall()

        return None
    except Error:
        if conexion and confirmar:
            conexion.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()
