import os
import json

import firebase_admin
from firebase_admin import credentials


def inicializar_firebase_admin():
    """Inicializa Firebase Admin una sola vez usando JSON en variable de entorno."""

    if firebase_admin._apps:
        return True

    firebase_credentials = (
        os.getenv("FIREBASE_CREDENTIALS") or ""
    ).strip()

    if not firebase_credentials:
        raise ValueError(
            "No existe la variable FIREBASE_CREDENTIALS"
        )

    cred_dict = json.loads(firebase_credentials)

    cred = credentials.Certificate(cred_dict)

    firebase_admin.initialize_app(cred)

    return True