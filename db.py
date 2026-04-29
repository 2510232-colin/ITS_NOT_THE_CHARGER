import os

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error


load_dotenv()


def obtener_configuracion_bd():
    return {
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "database": os.getenv("MYSQL_DATABASE", "techcare_db"),
        "autocommit": False,
    }


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
