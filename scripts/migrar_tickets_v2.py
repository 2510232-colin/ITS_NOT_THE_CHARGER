from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from db import obtener_conexion


def main():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("SHOW COLUMNS FROM tickets")
        existentes = {fila[0] for fila in cursor.fetchall()}

        alteraciones = []
        if "precio_estimado_referencial" not in existentes:
            alteraciones.append("ADD COLUMN precio_estimado_referencial DECIMAL(10,2) NULL AFTER descripcion")
        if "detalle_precio_estimado" not in existentes:
            alteraciones.append("ADD COLUMN detalle_precio_estimado VARCHAR(220) NULL AFTER precio_estimado_referencial")
        if "acepta_politica_domicilio" not in existentes:
            alteraciones.append("ADD COLUMN acepta_politica_domicilio TINYINT(1) NOT NULL DEFAULT 0 AFTER detalle_precio_estimado")

        if alteraciones:
            sentencia = f"ALTER TABLE tickets {', '.join(alteraciones)}"
            cursor.execute(sentencia)
            conexion.commit()
            print("Migración tickets v2 aplicada correctamente.")
        else:
            print("Tickets ya estaba actualizado. Sin cambios.")
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":
    main()
