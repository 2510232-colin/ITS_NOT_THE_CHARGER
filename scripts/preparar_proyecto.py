from pathlib import Path
import subprocess
import sys


BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"

SCRIPTS_BASE = [
    "inicializar_bd.py",
    "migrar_admin_v1.py",
    "migrar_roles_tecnico_v1.py",
    "migrar_tickets_v2.py",
    "migrar_contactos_v2.py",
    "migrar_servicios_v2.py",
    "migrar_servicios_v3.py",
    "migrar_ticket_mensajes_v1.py",
]


def ejecutar_script(nombre_script):
    ruta_script = SCRIPTS_DIR / nombre_script
    print(f"\n[INFO] Ejecutando: {nombre_script}")
    subprocess.run([sys.executable, str(ruta_script)], check=True, cwd=str(BASE_DIR))


def main():
    cargar_demo = "--demo" in sys.argv

    print("=" * 70)
    print("PREPARACIÓN DEL PROYECTO TECHCARE")
    print("=" * 70)
    print("Este script inicializa la base de datos y aplica migraciones.")
    if cargar_demo:
        print("Modo demo: también se cargará catálogo de servicios.")
    else:
        print("Modo normal: no se insertarán datos demo de servicios.")

    try:
        for nombre in SCRIPTS_BASE:
            ejecutar_script(nombre)

        if cargar_demo:
            ejecutar_script("cargar_catalogo_servicios.py")

        print("\n[SUCCESS] Proyecto preparado correctamente.")
        print("Puedes iniciar el servidor con: python server.py")
    except subprocess.CalledProcessError as error:
        print("\n[ERROR] Ocurrió un problema al preparar el proyecto.")
        print(f"Script con error: {error.cmd}")
        print("Revisa variables de entorno y conexión MySQL en tu archivo .env")
        sys.exit(1)


if __name__ == "__main__":
    main()
