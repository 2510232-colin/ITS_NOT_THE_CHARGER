from pathlib import Path
import re
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from db import obtener_conexion


def palabras_base(nombre, categoria, descripcion):
    texto = f"{nombre} {categoria} {descripcion}".lower()
    tokens = re.findall(r"[a-záéíóúüñ0-9]+", texto)
    tokens = [t for t in tokens if len(t) >= 4]

    extras = set()
    reglas = {
        "lenta": ["rendimiento", "optimización", "ssd", "ram", "mantenimiento"],
        "optim": ["computadora lenta", "rendimiento", "ssd", "ram"],
        "formate": ["sistema", "lenta", "arranque", "virus"],
        "sobrecal": ["se calienta", "ventilador", "pasta térmica", "limpieza"],
        "temperatura": ["sobrecalentamiento", "ventilador", "mantenimiento"],
        "ram": ["memoria", "multitarea", "rendimiento"],
        "ssd": ["disco", "arranque", "rapidez", "rendimiento"],
        "disco": ["almacenamiento", "ssd", "respaldo"],
        "virus": ["malware", "seguridad", "limpieza", "formateo"],
        "pantalla": ["display", "video", "imagen"],
        "enciende": ["fuente", "placa", "diagnóstico"],
    }

    for clave, vals in reglas.items():
        if clave in texto:
            extras.update(vals)

    salida = []
    vistos = set()
    for token in tokens + list(extras):
        token_l = token.strip().lower()
        if token_l and token_l not in vistos:
            vistos.add(token_l)
            salida.append(token)
        if len(salida) >= 16:
            break

    return ", ".join(salida)


def main():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("SHOW COLUMNS FROM servicios")
        existentes = {fila["Field"] for fila in cursor.fetchall()}

        alteraciones = []
        if "palabras_clave" not in existentes:
            alteraciones.append("ADD COLUMN palabras_clave VARCHAR(500) NULL AFTER tiempo_estimado")
        if "destacado_inicio" not in existentes:
            alteraciones.append("ADD COLUMN destacado_inicio TINYINT(1) NOT NULL DEFAULT 0 AFTER palabras_clave")
        if "orden_destacado" not in existentes:
            alteraciones.append("ADD COLUMN orden_destacado INT NOT NULL DEFAULT 0 AFTER destacado_inicio")
        if "promocion_activa" not in existentes:
            alteraciones.append("ADD COLUMN promocion_activa TINYINT(1) NOT NULL DEFAULT 0 AFTER orden_destacado")
        if "promocion_texto" not in existentes:
            alteraciones.append("ADD COLUMN promocion_texto VARCHAR(180) NULL AFTER promocion_activa")

        if alteraciones:
            cursor.execute(f"ALTER TABLE servicios {', '.join(alteraciones)}")

        cursor.execute("SELECT id, nombre, categoria, COALESCE(descripcion, '') AS descripcion, COALESCE(palabras_clave, '') AS palabras_clave FROM servicios")
        servicios = cursor.fetchall()

        for servicio in servicios:
            if servicio["palabras_clave"].strip():
                continue
            claves = palabras_base(servicio["nombre"], servicio["categoria"], servicio["descripcion"])
            cursor.execute(
                "UPDATE servicios SET palabras_clave = %s WHERE id = %s",
                (claves, servicio["id"]),
            )

        conexion.commit()
        print("Migración servicios v3 aplicada correctamente.")
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":
    main()
