import os

from flask import Flask, session, url_for
from dotenv import load_dotenv

from app_core import (
    NEGOCIO,
    POLITICA_DOMICILIO,
    asegurar_modelo_tickets,
    normalizar_rol,
)
from panel_routes import registrar_rutas_panel
from routes_auth import registrar_rutas_auth
from routes_public import registrar_rutas_publicas


app = Flask(__name__)
load_dotenv()
app.config["SECRET_KEY"] = os.getenv("CLAVE_SECRETA", "cambio-en-produccion")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.getenv("SESSION_COOKIE_SECURE", "0") == "1"


@app.context_processor
def inyectar_datos_globales():
    rol = normalizar_rol(session.get("rol"))
    panel_url = None
    if rol == "administrador":
        panel_url = url_for("admin_dashboard")
    elif rol == "tecnico":
        panel_url = url_for("tecnico_dashboard")
    elif rol == "cliente":
        panel_url = url_for("cliente_dashboard")

    return {
        "negocio": NEGOCIO,
        "usuario_actual": {
            "id": session.get("usuario_id"),
            "nombres": session.get("nombres"),
            "rol": rol,
        },
        "panel_url": panel_url,
        "politica_domicilio": POLITICA_DOMICILIO,
    }


registrar_rutas_publicas(app)
registrar_rutas_auth(app)
registrar_rutas_panel(app)
asegurar_modelo_tickets()


if __name__ == "__main__":
    debug_habilitado = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=8080, debug=debug_habilitado)
