from flask import flash, redirect, render_template, request, session, url_for
from mysql.connector import Error

from app_core import (
    construir_detalle_ampliado_servicio,
    construir_etiqueta_precio,
    enriquecer_servicios,
    estimar_ticket_por_texto,
    generar_folio_ticket,
    obtener_categorias_servicios,
    obtener_contenido_sitio,
    recomendar_servicios_por_palabras,
    requiere_sesion,
)
from db import ejecutar_consulta
from validaciones import limpiar_texto, validar_correo, validar_nombre, validar_texto_seguro


def registrar_rutas_publicas(app):
    @app.route("/")
    def inicio():
        try:
            servicios = ejecutar_consulta(
                """
                SELECT id, categoria, nombre AS titulo, descripcion, tipo_precio, precio, precio_min, precio_max,
                       destacado_inicio, orden_destacado, promocion_activa, promocion_texto
                FROM servicios
                WHERE activo = 1 AND destacado_inicio = 1
                ORDER BY orden_destacado ASC, id DESC
                LIMIT 6
                """,
                varias_filas=True,
            )
            if not servicios:
                servicios = ejecutar_consulta(
                    """
                    SELECT id, categoria, nombre AS titulo, descripcion, tipo_precio, precio, precio_min, precio_max,
                           destacado_inicio, orden_destacado, promocion_activa, promocion_texto
                    FROM servicios WHERE activo = 1 ORDER BY id DESC LIMIT 6
                    """,
                    varias_filas=True,
                )

            promociones = ejecutar_consulta(
                """
                SELECT id, nombre AS titulo, promocion_texto
                FROM servicios
                WHERE activo = 1 AND promocion_activa = 1 AND promocion_texto IS NOT NULL AND promocion_texto <> ''
                ORDER BY id DESC
                LIMIT 6
                """,
                varias_filas=True,
            )
            servicios = enriquecer_servicios(servicios)
        except Error:
            servicios = []
            promociones = []

        contenido_inicio = obtener_contenido_sitio()

        return render_template(
            "index.html",
            servicios=servicios,
            promociones=promociones,
            contenido_inicio=contenido_inicio,
            seccion_activa="inicio",
        )

    @app.route("/servicios")
    def servicios():
        busqueda = limpiar_texto(request.args.get("q", ""))[:140]
        categorias = []
        recomendaciones = []

        try:
            categorias = obtener_categorias_servicios()

            if busqueda:
                consulta_recomendador = """
                    SELECT id, categoria, nombre AS titulo, descripcion, tipo_precio, precio, precio_min, precio_max,
                          requiere_diagnostico, modalidad, tiempo_estimado, palabras_clave
                    FROM servicios
                    WHERE activo = 1
                """
                catalogo_recomendador = ejecutar_consulta(
                    consulta_recomendador,
                    varias_filas=True,
                )
                recomendaciones = recomendar_servicios_por_palabras(busqueda, catalogo_recomendador, limite=4)
                recomendaciones = enriquecer_servicios(recomendaciones)
        except Error:
            categorias = []
            recomendaciones = []

        return render_template(
            "servicios.html",
            categorias=categorias,
            busqueda=busqueda,
            recomendaciones=recomendaciones,
            seccion_activa="servicios",
        )

    @app.route("/servicios/categoria/<slug>")
    def servicios_por_categoria(slug):
        busqueda = limpiar_texto(request.args.get("q", ""))[:140]

        try:
            categorias = obtener_categorias_servicios()
        except Error:
            categorias = []

        categoria_objetivo = next((item for item in categorias if item["slug"] == slug), None)
        if not categoria_objetivo:
            flash("La categoría seleccionada no existe o no está disponible.", "error")
            return redirect(url_for("servicios"))

        categoria_nombre = categoria_objetivo["categoria"]
        try:
            consulta = """
                SELECT id, categoria, nombre AS titulo, descripcion, tipo_precio, precio, precio_min, precio_max,
                         requiere_diagnostico, modalidad, tiempo_estimado, palabras_clave
                FROM servicios
                WHERE activo = 1 AND categoria = %s
            """
            parametros = [categoria_nombre]
            if busqueda:
                consulta += " AND (nombre LIKE %s OR descripcion LIKE %s)"
                filtro = f"%{busqueda}%"
                parametros.extend([filtro, filtro])

            consulta += " ORDER BY nombre ASC"
            servicios_lista = ejecutar_consulta(consulta, tuple(parametros), varias_filas=True)
            servicios_lista = enriquecer_servicios(servicios_lista)
        except Error:
            servicios_lista = []

        return render_template(
            "servicios_categoria.html",
            categorias=categorias,
            categoria_activa_slug=slug,
            categoria_activa_nombre=categoria_nombre,
            busqueda=busqueda,
            servicios=servicios_lista,
            seccion_activa="servicios",
        )

    @app.route("/servicios/detalle")
    def servicio_detalle():
        id_servicio = limpiar_texto(request.args.get("id", ""))
        try:
            if id_servicio.isdigit():
                servicio = ejecutar_consulta(
                    """
                    SELECT id, categoria, nombre AS titulo, descripcion, tipo_precio, precio, precio_min, precio_max,
                          requiere_diagnostico, modalidad, tiempo_estimado, palabras_clave
                    FROM servicios
                    WHERE id = %s AND activo = 1
                    LIMIT 1
                    """,
                    (int(id_servicio),),
                    una_fila=True,
                )
            else:
                servicio = ejecutar_consulta(
                    """
                    SELECT id, categoria, nombre AS titulo, descripcion, tipo_precio, precio, precio_min, precio_max,
                          requiere_diagnostico, modalidad, tiempo_estimado, palabras_clave
                    FROM servicios
                    WHERE activo = 1
                    ORDER BY id DESC LIMIT 1
                    """,
                    una_fila=True,
                )
            if servicio:
                servicio["precio_mostrar"] = construir_etiqueta_precio(servicio)
                servicio["detalle_extendido"] = construir_detalle_ampliado_servicio(servicio)
        except Error:
            servicio = None

        return render_template("servicio_detalle.html", servicio=servicio, seccion_activa="servicios")

    @app.route("/productos")
    def productos():
        try:
            productos_lista = ejecutar_consulta(
                "SELECT id, nombre AS titulo, descripcion, precio FROM productos WHERE activo = 1 ORDER BY id DESC",
                varias_filas=True,
            )
        except Error:
            productos_lista = []

        return render_template("productos.html", productos=productos_lista, seccion_activa="productos")

    @app.route("/productos/detalle")
    def producto_detalle():
        try:
            producto = ejecutar_consulta(
                "SELECT id, nombre AS titulo, descripcion, precio FROM productos WHERE activo = 1 ORDER BY id DESC LIMIT 1",
                una_fila=True,
            )
        except Error:
            producto = None

        return render_template("producto_detalle.html", producto=producto, seccion_activa="productos")

    @app.route("/nosotros")
    def nosotros():
        return render_template("nosotros.html", seccion_activa="nosotros")

    @app.route("/contacto", methods=["GET", "POST"])
    def contacto():
        if request.method == "POST":
            nombre = limpiar_texto(request.form.get("nombre"))
            correo = limpiar_texto(request.form.get("correo"))
            mensaje = limpiar_texto(request.form.get("mensaje"))

            ok, error = validar_nombre(nombre)
            if not ok:
                flash(error, "error")
                return redirect(url_for("contacto"))

            ok, error = validar_correo(correo)
            if not ok:
                flash(error, "error")
                return redirect(url_for("contacto"))

            ok, error = validar_texto_seguro(mensaje, "mensaje", 10, 1000)
            if not ok:
                flash(error, "error")
                return redirect(url_for("contacto"))

            try:
                ejecutar_consulta(
                    "INSERT INTO contactos (nombre, correo, mensaje) VALUES (%s, %s, %s)",
                    (nombre, correo.lower(), mensaje),
                    confirmar=True,
                )
                flash("Tu mensaje fue enviado correctamente.", "exito")
            except Error:
                flash("No fue posible guardar tu mensaje en este momento.", "error")

            return redirect(url_for("contacto"))

        return render_template("contacto.html", seccion_activa="contacto")

    @app.route("/cotizacion", methods=["GET", "POST"])
    def cotizacion():
        if not requiere_sesion():
            flash("Debes iniciar sesión para generar una cotización.", "error")
            return redirect(url_for("login"))

        if request.method == "POST":
            servicio_requerido = limpiar_texto(request.form.get("servicio_requerido"))
            equipo = limpiar_texto(request.form.get("equipo"))
            descripcion_problema = limpiar_texto(request.form.get("descripcion_problema"))
            acepta_politica_domicilio = request.form.get("acepta_politica_domicilio")

            ok, error = validar_texto_seguro(servicio_requerido, "servicio", 3, 140)
            if not ok:
                flash(error, "error")
                return redirect(url_for("cotizacion"))

            ok, error = validar_texto_seguro(equipo, "equipo", 2, 140)
            if not ok:
                flash(error, "error")
                return redirect(url_for("cotizacion"))

            ok, error = validar_texto_seguro(descripcion_problema, "descripción", 10, 2000)
            if not ok:
                flash(error, "error")
                return redirect(url_for("cotizacion"))

            if acepta_politica_domicilio != "on":
                flash("Debes aceptar la política de servicio a domicilio para continuar.", "error")
                return redirect(url_for("cotizacion"))

            estimado_referencial, detalle_estimado = estimar_ticket_por_texto(
                servicio_requerido,
                equipo,
                descripcion_problema,
            )

            try:
                folio_ticket = generar_folio_ticket()
                id_ticket = ejecutar_consulta(
                    """
                    INSERT INTO tickets (
                        folio, id_usuario, servicio_solicitado, equipo, descripcion, estado,
                        precio_estimado_referencial, detalle_precio_estimado, acepta_politica_domicilio
                    )
                    VALUES (%s, %s, %s, %s, %s, 'Recibido', %s, %s, %s)
                    """,
                    (
                        folio_ticket,
                        session.get("usuario_id"),
                        servicio_requerido,
                        equipo,
                        descripcion_problema,
                        estimado_referencial,
                        detalle_estimado,
                        1,
                    ),
                    confirmar=True,
                )
                flash(f"Ticket generado: {folio_ticket}. Estimado referencial: {detalle_estimado}.", "exito")
                return redirect(url_for("ticket_detalle", id_ticket=id_ticket))
            except Error:
                flash("No fue posible generar el ticket. Verifica conexión a base de datos.", "error")

        return render_template("cotizacion.html", seccion_activa="servicios")

    @app.route("/carrito")
    def carrito():
        return render_template("carrito.html", seccion_activa="productos")

    @app.route("/mi-cuenta")
    def mi_cuenta():
        if not requiere_sesion():
            flash("Debes iniciar sesión para acceder a tu cuenta.", "error")
            return redirect(url_for("login"))

        return render_template("mi_cuenta.html", seccion_activa="inicio")

    @app.route("/<path:ruta_antigua>.html")
    def compatibilidad_rutas_antiguas(ruta_antigua):
        mapa_redireccion = {
            "index": "inicio",
            "servicios": "servicios",
            "servicio_detalle": "servicio_detalle",
            "productos": "productos",
            "producto_detalle": "producto_detalle",
            "nosotros": "nosotros",
            "contacto": "contacto",
            "cotizacion": "cotizacion",
            "carrito": "carrito",
            "login": "login",
            "registro": "registro",
            "cliente_dashboard": "cliente_dashboard",
            "admin_dashboard": "admin_dashboard",
            "gestor_dashboard": "tecnico_dashboard",
            "tecnico_dashboard": "tecnico_dashboard",
            "tickets": "tickets",
        }

        endpoint = mapa_redireccion.get(ruta_antigua)
        if endpoint:
            return redirect(url_for(endpoint))

        return redirect(url_for("inicio"))
