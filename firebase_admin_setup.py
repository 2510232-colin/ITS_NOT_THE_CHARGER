import os

import firebase_admin
from firebase_admin import credentials


def inicializar_firebase_admin():
    """Inicializa Firebase Admin una sola vez usando ruta de credenciales en variable de entorno."""
    if firebase_admin._apps:
        return True

    cred_path = (os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH") or "").strip()
    if not cred_path:
        return False

    if not os.path.exists(cred_path):
        raise FileNotFoundError(
            f"No se encontro el archivo de credenciales Firebase: {cred_path}"
        )

    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    return True
