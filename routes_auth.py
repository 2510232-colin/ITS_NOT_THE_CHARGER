import os

from flask import flash, jsonify, redirect, render_template, request, session, url_for
from firebase_admin import auth as firebase_auth
from mysql.connector import Error
from werkzeug.security import check_password_hash, generate_password_hash

from app_core import normalizar_rol, redireccion_por_rol
from db import ejecutar_consulta
from validaciones import (
    limpiar_texto,
    validar_contrasena,
    validar_correo,
    validar_nombre,
    validar_telefono,
)


def registrar_rutas_auth(app):
    def _abrir_sesion_local(usuario):
        session["usuario_id"] = usuario["id"]
        session["rol"] = normalizar_rol(usuario["rol"])
        session["nombres"] = usuario["nombres"]

    @app.route("/registro", methods=["GET", "POST"])
    def registro():
        if request.method == "POST":
            nombre = limpiar_texto(request.form.get("nombre"))
            apellidos = limpiar_texto(request.form.get("apellidos"))
            correo = limpiar_texto(request.form.get("correo")).lower()
            telefono = limpiar_texto(request.form.get("telefono"))
            contrasena = request.form.get("contrasena", "")
            confirmar_contrasena = request.form.get("confirmar_contrasena", "")

            for valor, etiqueta in ((nombre, "nombre"), (apellidos, "apellidos")):
                ok, error = validar_nombre(valor, etiqueta)
                if not ok:
                    flash(error, "error")
                    return redirect(url_for("registro"))

            ok, error = validar_correo(correo)
            if not ok:
                flash(error, "error")
                return redirect(url_for("registro"))

            ok, error = validar_telefono(telefono)
            if not ok:
                flash(error, "error")
                return redirect(url_for("registro"))

            ok, error = validar_contrasena(contrasena)
            if not ok:
                flash(error, "error")
                return redirect(url_for("registro"))

            if contrasena != confirmar_contrasena:
                flash("Las contraseñas no coinciden.", "error")
                return redirect(url_for("registro"))

            try:
                usuario_existente = ejecutar_consulta(
                    "SELECT id FROM usuarios WHERE correo = %s",
                    (correo,),
                    una_fila=True,
                )
                if usuario_existente:
                    flash("Ese correo ya está registrado.", "error")
                    return redirect(url_for("registro"))

                hash_contrasena = generate_password_hash(contrasena)
                ejecutar_consulta(
                    """
                    INSERT INTO usuarios (correo, contrasena_hash, nombres, apellidos, numero, rol, activo)
                    VALUES (%s, %s, %s, %s, %s, 'cliente', 1)
                    """,
                    (correo, hash_contrasena, nombre, apellidos, telefono),
                    confirmar=True,
                )
                flash("Cuenta creada correctamente. Ahora puedes iniciar sesión.", "exito")
                return redirect(url_for("login"))
            except Error:
                flash("No fue posible registrar tu cuenta. Verifica la conexión MySQL.", "error")

        return render_template("registro.html", seccion_activa="inicio")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            correo = limpiar_texto(request.form.get("correo")).lower()
            contrasena = request.form.get("contrasena", "")

            ok, error = validar_correo(correo)
            if not ok:
                flash(error, "error")
                return redirect(url_for("login"))

            if not contrasena:
                flash("La contraseña es obligatoria.", "error")
                return redirect(url_for("login"))

            try:
                usuario = ejecutar_consulta(
                    "SELECT id, correo, contrasena_hash, nombres, rol, activo FROM usuarios WHERE correo = %s LIMIT 1",
                    (correo,),
                    una_fila=True,
                )
            except Error:
                flash("No fue posible conectar con la base de datos.", "error")
                return redirect(url_for("login"))

            if not usuario or not usuario["activo"]:
                flash("Credenciales inválidas.", "error")
                return redirect(url_for("login"))

            if not check_password_hash(usuario["contrasena_hash"], contrasena):
                flash("Credenciales inválidas.", "error")
                return redirect(url_for("login"))

            _abrir_sesion_local(usuario)

            return redirect(redireccion_por_rol(usuario["rol"]))

        return render_template("login.html", seccion_activa="inicio")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Sesión cerrada correctamente.", "exito")
        return redirect(url_for("inicio"))

    @app.route("/auth/firebase/google", methods=["POST"])
    def auth_firebase_google():
        data = request.get_json(silent=True) or {}
        id_token = (data.get("token") or "").strip()
        if not id_token:
            return jsonify({"ok": False, "mensaje": "Token faltante."}), 400

        try:
            decoded = firebase_auth.verify_id_token(id_token)
        except Exception:
            return jsonify({"ok": False, "mensaje": "Token inválido de Firebase."}), 401

        firebase_uid = (decoded.get("uid") or "").strip()
        correo = (decoded.get("email") or "").strip().lower()
        nombre_completo = limpiar_texto(decoded.get("name") or "Usuario")
        nombres = nombre_completo
        apellidos = ""

        if " " in nombre_completo:
            partes = nombre_completo.split(" ", 1)
            nombres = partes[0]
            apellidos = partes[1]

        if not firebase_uid or not correo:
            return jsonify({"ok": False, "mensaje": "El token no contiene datos suficientes."}), 400

        try:
            usuario = ejecutar_consulta(
                """
                SELECT id, correo, nombres, rol, activo
                FROM usuarios
                WHERE firebase_uid = %s
                LIMIT 1
                """,
                (firebase_uid,),
                una_fila=True,
            )

            if not usuario:
                usuario = ejecutar_consulta(
                    """
                    SELECT id, correo, nombres, rol, activo
                    FROM usuarios
                    WHERE correo = %s
                    LIMIT 1
                    """,
                    (correo,),
                    una_fila=True,
                )

                if usuario:
                    ejecutar_consulta(
                        """
                        UPDATE usuarios
                        SET firebase_uid = %s, auth_provider = 'google'
                        WHERE id = %s
                        """,
                        (firebase_uid, usuario["id"]),
                        confirmar=True,
                    )

            if not usuario:
                hash_placeholder = generate_password_hash(os.urandom(24).hex())
                usuario_id = ejecutar_consulta(
                    """
                    INSERT INTO usuarios (
                        correo, contrasena_hash, nombres, apellidos, numero, rol, activo, firebase_uid, auth_provider
                    )
                    VALUES (%s, %s, %s, %s, '', 'cliente', 1, %s, 'google')
                    """,
                    (correo, hash_placeholder, nombres, apellidos, firebase_uid),
                    confirmar=True,
                )
                usuario = ejecutar_consulta(
                    """
                    SELECT id, correo, nombres, rol, activo
                    FROM usuarios
                    WHERE id = %s
                    LIMIT 1
                    """,
                    (usuario_id,),
                    una_fila=True,
                )

            if not usuario or not usuario.get("activo"):
                return jsonify({"ok": False, "mensaje": "Usuario no disponible para iniciar sesión."}), 403

            _abrir_sesion_local(usuario)
            return jsonify({"ok": True, "redirect": redireccion_por_rol(usuario["rol"])})
        except Error:
            return jsonify({"ok": False, "mensaje": "No fue posible procesar inicio con Google."}), 500
