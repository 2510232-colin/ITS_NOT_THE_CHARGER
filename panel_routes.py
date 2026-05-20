from flask import flash, redirect, render_template, request, session, url_for
from mysql.connector import Error
from werkzeug.security import generate_password_hash

from app_core import (
    ESTADOS_ORDEN_ACTIVA,
    ESTADOS_ORDEN_CERRADA,
    ESTADOS_SOLICITUD,
    ESTADOS_PEDIDO,
    ESTADOS_TICKET,
    asegurar_modelo_tickets,
    cambiar_estado_ticket,
    convertir_ticket_a_orden,
    estado_a_clase,
    es_orden_activa,
    es_solicitud_ticket,
    es_trabajo_finalizado,
    obtener_contenido_sitio,
    obtener_historial_ticket,
    obtener_mensajes_ticket,
    obtener_ticket_por_id,
    obtener_tickets_usuario,
    redireccion_por_rol,
    requiere_rol,
    requiere_sesion,
    verificar_acceso_admin,
    verificar_acceso_operativo,
)
from db import ejecutar_consulta
from validaciones import (
    limpiar_texto,
    validar_contrasena,
    validar_correo,
    validar_nombre,
    validar_telefono,
    validar_texto_seguro,
)


CATEGORIAS_SERVICIO = [
    "Reparación y diagnóstico",
    "Mantenimiento preventivo y correctivo",
    "Software y sistema operativo",
    "Seguridad y optimización",
    "Respaldo y recuperación",
    "Upgrade y ensamblaje",
    "Redes y conectividad",
    "Servicios premium",
    "Servicios empresariales",
]


def registrar_rutas_panel(app):
    asegurar_modelo_tickets()

    @app.route("/panel/cliente")
    def cliente_dashboard():
        if not requiere_sesion():
            return redirect(url_for("login"))

        if not requiere_rol("cliente"):
            flash("Este módulo es exclusivo para clientes.", "error")
            return redirect(redireccion_por_rol(session.get("rol", "cliente")))

        tickets = obtener_tickets_usuario()
        try:
            total_pedidos = ejecutar_consulta(
                "SELECT COUNT(*) AS total FROM pedidos WHERE id_usuario = %s",
                (session.get("usuario_id"),),
                una_fila=True,
            )["total"]
            compras_entregadas = ejecutar_consulta(
                "SELECT COUNT(*) AS total FROM pedidos WHERE id_usuario = %s AND estado = 'Entregado'",
                (session.get("usuario_id"),),
                una_fila=True,
            )["total"]
        except Error:
            total_pedidos = 0
            compras_entregadas = 0

        return render_template(
            "cliente_dashboard.html",
            tickets=tickets,
            total_tickets=len(tickets),
            total_pedidos=total_pedidos,
            compras_entregadas=compras_entregadas,
            titulo_panel="INTC Cliente",
        )

    @app.route("/panel/mis-pedidos")
    def cliente_pedidos():
        if not requiere_sesion() or not requiere_rol("cliente"):
            flash("Este módulo es exclusivo para clientes.", "error")
            return redirect(redireccion_por_rol(session.get("rol", "cliente")))

        try:
            pedidos = ejecutar_consulta(
                """
                SELECT id, folio, total, estado, DATE_FORMAT(fecha_creacion, '%d/%m/%Y') AS fecha
                FROM pedidos
                WHERE id_usuario = %s
                ORDER BY id DESC
                """,
                (session.get("usuario_id"),),
                varias_filas=True,
            )
        except Error:
            pedidos = []
            flash("No fue posible cargar tus pedidos.", "error")

        return render_template(
            "cliente_pedidos.html",
            pedidos=pedidos,
            titulo_panel="INTC Cliente",
        )

    @app.route("/panel/admin")
    def admin_dashboard():
        acceso = verificar_acceso_admin()
        if acceso:
            return acceso

        tickets = obtener_tickets_usuario()
        total_productos = ejecutar_consulta("SELECT COUNT(*) AS total FROM productos", una_fila=True)["total"]
        total_servicios = ejecutar_consulta("SELECT COUNT(*) AS total FROM servicios", una_fila=True)["total"]
        total_usuarios = ejecutar_consulta("SELECT COUNT(*) AS total FROM usuarios", una_fila=True)["total"]
        solicitudes_pendientes = sum(1 for item in tickets if item.get("estado") == "Pendiente")
        ordenes_activas = sum(1 for item in tickets if es_orden_activa(item))
        trabajos_finalizados = sum(1 for item in tickets if es_trabajo_finalizado(item))
        try:
            total_pedidos = ejecutar_consulta("SELECT COUNT(*) AS total FROM pedidos", una_fila=True)["total"]
        except Error:
            total_pedidos = 0

        return render_template(
            "admin_dashboard.html",
            tickets=tickets,
            total_tickets=len(tickets),
            total_productos=total_productos,
            total_servicios=total_servicios,
            total_usuarios=total_usuarios,
            total_pedidos=total_pedidos,
            solicitudes_pendientes=solicitudes_pendientes,
            ordenes_activas=ordenes_activas,
            trabajos_finalizados=trabajos_finalizados,
            titulo_panel="INTC Admin",
        )

    @app.route("/panel/admin/productos", methods=["GET", "POST"])
    def admin_productos():
        acceso = verificar_acceso_admin()
        if acceso:
            return acceso

        if request.method == "POST":
            accion = limpiar_texto(request.form.get("accion"))
            id_item = limpiar_texto(request.form.get("id_item"))

            if accion == "eliminar" and id_item.isdigit():
                try:
                    ejecutar_consulta(
                        "DELETE FROM productos WHERE id = %s",
                        (int(id_item),),
                        confirmar=True,
                    )
                    flash("Producto eliminado correctamente.", "exito")
                except Error:
                    flash("No fue posible eliminar el producto.", "error")
                return redirect(url_for("admin_productos"))

            nombre = limpiar_texto(request.form.get("nombre"))
            descripcion = limpiar_texto(request.form.get("descripcion"))
            categoria = limpiar_texto(request.form.get("categoria"))
            precio = limpiar_texto(request.form.get("precio"))
            stock = limpiar_texto(request.form.get("stock"))

            if not all([nombre, descripcion, categoria, precio, stock]):
                flash("Completa todos los campos del producto.", "error")
                return redirect(url_for("admin_productos"))

            try:
                precio_num = float(precio)
                stock_num = int(stock)
            except ValueError:
                flash("Precio o stock inválidos.", "error")
                return redirect(url_for("admin_productos"))

            for valor, etiqueta in ((nombre, "nombre"), (categoria, "categoría"), (descripcion, "descripción")):
                ok, error = validar_texto_seguro(valor, etiqueta, 2, 2000)
                if not ok:
                    flash(error, "error")
                    return redirect(url_for("admin_productos"))

            if accion == "editar" and id_item.isdigit():
                try:
                    ejecutar_consulta(
                        """
                        UPDATE productos
                        SET nombre = %s, descripcion = %s, precio = %s, stock = %s
                        WHERE id = %s
                        """,
                        (f"[{categoria}] {nombre}", descripcion, precio_num, stock_num, int(id_item)),
                        confirmar=True,
                    )
                    flash("Producto actualizado correctamente.", "exito")
                except Error:
                    flash("No fue posible actualizar el producto.", "error")
            else:
                try:
                    ejecutar_consulta(
                        """
                        INSERT INTO productos (nombre, descripcion, precio, stock, activo)
                        VALUES (%s, %s, %s, %s, 1)
                        """,
                        (f"[{categoria}] {nombre}", descripcion, precio_num, stock_num),
                        confirmar=True,
                    )
                    flash("Producto agregado correctamente.", "exito")
                except Error:
                    flash("No fue posible agregar el producto.", "error")

            return redirect(url_for("admin_productos"))

        id_edicion = request.args.get("editar", "")
        producto_edicion = None
        try:
            productos = ejecutar_consulta(
                "SELECT id, nombre, descripcion, precio, stock FROM productos ORDER BY id DESC",
                varias_filas=True,
            )
        except Error:
            productos = []
            flash("No fue posible cargar productos desde la base de datos.", "error")

        if id_edicion.isdigit():
            producto_edicion = next((item for item in productos if item["id"] == int(id_edicion)), None)
            if producto_edicion and producto_edicion["nombre"].startswith("[") and "] " in producto_edicion["nombre"]:
                categoria, nombre = producto_edicion["nombre"].split("] ", 1)
                producto_edicion = {
                    **producto_edicion,
                    "categoria": categoria.replace("[", ""),
                    "nombre": nombre,
                }

        return render_template(
            "admin_productos.html",
            titulo_panel="INTC Admin",
            productos=productos,
            producto_edicion=producto_edicion,
        )

    @app.route("/panel/admin/servicios", methods=["GET", "POST"])
    def admin_servicios():
        acceso = verificar_acceso_admin()
        if acceso:
            return acceso

        if request.method == "POST":
            accion = limpiar_texto(request.form.get("accion"))
            id_item = limpiar_texto(request.form.get("id_item"))

            if accion == "eliminar" and id_item.isdigit():
                try:
                    ejecutar_consulta(
                        "DELETE FROM servicios WHERE id = %s",
                        (int(id_item),),
                        confirmar=True,
                    )
                    flash("Servicio eliminado correctamente.", "exito")
                except Error:
                    flash("No fue posible eliminar el servicio.", "error")
                return redirect(url_for("admin_servicios"))

            nombre = limpiar_texto(request.form.get("nombre"))
            descripcion = limpiar_texto(request.form.get("descripcion"))
            categoria = limpiar_texto(request.form.get("categoria"))
            precio = limpiar_texto(request.form.get("precio"))
            palabras_clave = limpiar_texto(request.form.get("palabras_clave"))
            destacado_inicio = 1 if request.form.get("destacado_inicio") == "on" else 0
            promocion_activa = 1 if request.form.get("promocion_activa") == "on" else 0
            promocion_texto = limpiar_texto(request.form.get("promocion_texto"))
            orden_destacado = limpiar_texto(request.form.get("orden_destacado")) or "0"

            if not all([nombre, descripcion, categoria, precio]):
                flash("Completa todos los campos del servicio.", "error")
                return redirect(url_for("admin_servicios"))

            if categoria not in CATEGORIAS_SERVICIO:
                flash("Selecciona una categoría válida del catálogo predefinido.", "error")
                return redirect(url_for("admin_servicios"))

            try:
                precio_num = float(precio)
                orden_destacado_num = int(orden_destacado)
            except ValueError:
                flash("Precio u orden de destacado inválidos.", "error")
                return redirect(url_for("admin_servicios"))

            for valor, etiqueta in ((nombre, "nombre"), (categoria, "categoría"), (descripcion, "descripción")):
                ok, error = validar_texto_seguro(valor, etiqueta, 2, 2000)
                if not ok:
                    flash(error, "error")
                    return redirect(url_for("admin_servicios"))

            if palabras_clave:
                ok, error = validar_texto_seguro(palabras_clave, "palabras clave", 3, 500)
                if not ok:
                    flash(error, "error")
                    return redirect(url_for("admin_servicios"))

            if promocion_activa and not promocion_texto:
                flash("Si activas promoción debes escribir su descripción.", "error")
                return redirect(url_for("admin_servicios"))

            if accion == "editar" and id_item.isdigit():
                try:
                    ejecutar_consulta(
                        """
                        UPDATE servicios
                        SET nombre = %s,
                            categoria = %s,
                            descripcion = %s,
                            precio = %s,
                            palabras_clave = %s,
                            destacado_inicio = %s,
                            orden_destacado = %s,
                            promocion_activa = %s,
                            promocion_texto = %s
                        WHERE id = %s
                        """,
                        (
                            nombre,
                            categoria,
                            descripcion,
                            precio_num,
                            palabras_clave,
                            destacado_inicio,
                            orden_destacado_num,
                            promocion_activa,
                            promocion_texto,
                            int(id_item),
                        ),
                        confirmar=True,
                    )
                    flash("Servicio actualizado correctamente.", "exito")
                except Error:
                    flash("No fue posible actualizar el servicio.", "error")
            else:
                try:
                    ejecutar_consulta(
                        """
                        INSERT INTO servicios (
                            categoria, nombre, descripcion, precio,
                            palabras_clave, destacado_inicio, orden_destacado,
                            promocion_activa, promocion_texto, activo
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
                        """,
                        (
                            categoria,
                            nombre,
                            descripcion,
                            precio_num,
                            palabras_clave,
                            destacado_inicio,
                            orden_destacado_num,
                            promocion_activa,
                            promocion_texto,
                        ),
                        confirmar=True,
                    )
                    flash("Servicio agregado correctamente.", "exito")
                except Error:
                    flash("No fue posible agregar el servicio.", "error")

            return redirect(url_for("admin_servicios"))

        filtro_q = limpiar_texto(request.args.get("q", ""))
        id_edicion = request.args.get("editar", "")
        servicio_edicion = None
        try:
            consulta = """
                SELECT id, categoria, nombre, descripcion, precio, palabras_clave,
                       destacado_inicio, orden_destacado, promocion_activa, promocion_texto
                FROM servicios
            """
            parametros = []
            if filtro_q:
                consulta += " WHERE nombre LIKE %s OR descripcion LIKE %s OR categoria LIKE %s"
                like = f"%{filtro_q}%"
                parametros.extend([like, like, like])

            consulta += " ORDER BY destacado_inicio DESC, orden_destacado ASC, id DESC"
            servicios = ejecutar_consulta(consulta, tuple(parametros), varias_filas=True)
        except Error:
            servicios = []
            flash("No fue posible cargar servicios desde la base de datos.", "error")

        if id_edicion.isdigit():
            try:
                servicio_edicion = ejecutar_consulta(
                    """
                    SELECT id, categoria, nombre, descripcion, precio, palabras_clave,
                           destacado_inicio, orden_destacado, promocion_activa, promocion_texto
                    FROM servicios
                    WHERE id = %s
                    LIMIT 1
                    """,
                    (int(id_edicion),),
                    una_fila=True,
                )
            except Error:
                servicio_edicion = None

        return render_template(
            "admin_servicios.html",
            titulo_panel="INTC Admin",
            servicios=servicios,
            servicio_edicion=servicio_edicion,
            filtro_q=filtro_q,
            categorias_servicio=CATEGORIAS_SERVICIO,
        )

    @app.route("/panel/admin/pedidos", methods=["GET", "POST"])
    def admin_pedidos():
        acceso = verificar_acceso_admin()
        if acceso:
            return acceso

        if request.method == "POST":
            id_pedido = limpiar_texto(request.form.get("id_pedido"))
            nuevo_estado = limpiar_texto(request.form.get("nuevo_estado"))

            if not id_pedido.isdigit() or nuevo_estado not in ESTADOS_PEDIDO:
                flash("Datos de pedido inválidos.", "error")
                return redirect(url_for("admin_pedidos"))

            try:
                pedido = ejecutar_consulta(
                    "SELECT id FROM pedidos WHERE id = %s",
                    (int(id_pedido),),
                    una_fila=True,
                )
                if not pedido:
                    flash("El pedido indicado no existe.", "error")
                    return redirect(url_for("admin_pedidos"))

                ejecutar_consulta(
                    "UPDATE pedidos SET estado = %s WHERE id = %s",
                    (nuevo_estado, int(id_pedido)),
                    confirmar=True,
                )
                flash("Estado del pedido actualizado correctamente.", "exito")
            except Error:
                flash("No fue posible actualizar el pedido.", "error")

            return redirect(url_for("admin_pedidos"))

        try:
            pedidos = ejecutar_consulta(
                """
                SELECT p.id, p.folio, CONCAT(u.nombres, ' ', u.apellidos) AS cliente, p.total, p.estado
                FROM pedidos p
                INNER JOIN usuarios u ON u.id = p.id_usuario
                ORDER BY p.id DESC
                """,
                varias_filas=True,
            )
        except Error:
            pedidos = []
            flash("No fue posible cargar pedidos desde base de datos.", "error")

        return render_template(
            "admin_pedidos.html",
            titulo_panel="INTC Admin",
            pedidos=pedidos,
            estados_pedido=ESTADOS_PEDIDO,
        )

    @app.route("/panel/admin/contenido", methods=["GET", "POST"])
    def admin_contenido():
        acceso = verificar_acceso_admin()
        if acceso:
            return acceso

        if request.method == "POST":
            titulo_hero = limpiar_texto(request.form.get("titulo_hero"))
            subtitulo_hero = limpiar_texto(request.form.get("subtitulo_hero"))
            mensaje_promocional = limpiar_texto(request.form.get("mensaje_promocional"))

            if not all([titulo_hero, subtitulo_hero, mensaje_promocional]):
                flash("Completa todos los campos de contenido.", "error")
                return redirect(url_for("admin_contenido"))

            try:
                ejecutar_consulta(
                    """
                    INSERT INTO contenido_sitio (id, titulo_hero, subtitulo_hero, mensaje_promocional)
                    VALUES (1, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        titulo_hero = VALUES(titulo_hero),
                        subtitulo_hero = VALUES(subtitulo_hero),
                        mensaje_promocional = VALUES(mensaje_promocional)
                    """,
                    (titulo_hero, subtitulo_hero, mensaje_promocional),
                    confirmar=True,
                )
                flash("Contenido del sitio actualizado correctamente.", "exito")
            except Error:
                flash("No fue posible actualizar contenido en base de datos.", "error")
            return redirect(url_for("admin_contenido"))

        contenido = obtener_contenido_sitio()

        return render_template(
            "admin_contenido.html",
            titulo_panel="INTC Admin",
            contenido=contenido,
        )

    @app.route("/panel/admin/usuarios", methods=["GET", "POST"])
    def admin_usuarios():
        acceso = verificar_acceso_admin()
        if acceso:
            return acceso

        if request.method == "POST":
            accion = limpiar_texto(request.form.get("accion"))

            if accion == "eliminar":
                id_usuario = limpiar_texto(request.form.get("id_usuario"))
                if not id_usuario.isdigit():
                    flash("Usuario inválido para eliminación.", "error")
                    return redirect(url_for("admin_usuarios"))

                if int(id_usuario) == session.get("usuario_id"):
                    flash("No puedes eliminar tu propio usuario en sesión.", "error")
                    return redirect(url_for("admin_usuarios"))

                try:
                    ejecutar_consulta(
                        "DELETE FROM usuarios WHERE id = %s",
                        (int(id_usuario),),
                        confirmar=True,
                    )
                    flash("Usuario eliminado correctamente.", "exito")
                except Error:
                    flash("No fue posible eliminar el usuario. Verifica dependencias (tickets/pedidos).", "error")
                return redirect(url_for("admin_usuarios"))

            if accion == "cambiar_rol":
                id_usuario = limpiar_texto(request.form.get("id_usuario"))
                nuevo_rol = limpiar_texto(request.form.get("nuevo_rol"))
                if id_usuario.isdigit() and nuevo_rol in ["administrador", "tecnico", "cliente"]:
                    try:
                        ejecutar_consulta(
                            "UPDATE usuarios SET rol = %s WHERE id = %s",
                            (nuevo_rol, int(id_usuario)),
                            confirmar=True,
                        )
                        flash("Rol de usuario actualizado correctamente.", "exito")
                    except Error:
                        flash("No fue posible actualizar el rol del usuario.", "error")
                else:
                    flash("Datos inválidos para cambio de rol.", "error")
                return redirect(url_for("admin_usuarios"))

            correo = limpiar_texto(request.form.get("correo"))
            nombres = limpiar_texto(request.form.get("nombres"))
            apellidos = limpiar_texto(request.form.get("apellidos"))
            numero = limpiar_texto(request.form.get("numero"))
            contrasena = request.form.get("contrasena", "")
            rol = limpiar_texto(request.form.get("rol"))

            if not all([correo, nombres, apellidos, numero, contrasena, rol]):
                flash("Completa todos los campos del usuario.", "error")
                return redirect(url_for("admin_usuarios"))

            if rol not in ["administrador", "tecnico", "cliente"]:
                flash("Rol inválido.", "error")
                return redirect(url_for("admin_usuarios"))

            ok, error = validar_correo(correo)
            if not ok:
                flash(error, "error")
                return redirect(url_for("admin_usuarios"))

            for valor, etiqueta in ((nombres, "nombres"), (apellidos, "apellidos")):
                ok, error = validar_nombre(valor, etiqueta)
                if not ok:
                    flash(error, "error")
                    return redirect(url_for("admin_usuarios"))

            ok, error = validar_telefono(numero)
            if not ok:
                flash(error, "error")
                return redirect(url_for("admin_usuarios"))

            ok, error = validar_contrasena(contrasena)
            if not ok:
                flash(error, "error")
                return redirect(url_for("admin_usuarios"))

            try:
                existente = ejecutar_consulta(
                    "SELECT id FROM usuarios WHERE correo = %s",
                    (correo.lower(),),
                    una_fila=True,
                )
                if existente:
                    flash("El correo ya está registrado.", "error")
                    return redirect(url_for("admin_usuarios"))

                ejecutar_consulta(
                    """
                    INSERT INTO usuarios (correo, contrasena_hash, nombres, apellidos, numero, rol, activo)
                    VALUES (%s, %s, %s, %s, %s, %s, 1)
                    """,
                    (correo.lower(), generate_password_hash(contrasena), nombres, apellidos, numero, rol),
                    confirmar=True,
                )
                flash("Usuario agregado correctamente.", "exito")
            except Error:
                flash("No fue posible agregar el usuario.", "error")
            return redirect(url_for("admin_usuarios"))

        filtro_q = limpiar_texto(request.args.get("q", ""))
        filtro_rol = limpiar_texto(request.args.get("rol", ""))

        try:
            consulta = """
                SELECT id, correo, nombres, apellidos, numero, rol, activo
                FROM usuarios
                WHERE 1 = 1
            """
            parametros = []

            if filtro_q:
                consulta += " AND (correo LIKE %s OR nombres LIKE %s OR apellidos LIKE %s OR numero LIKE %s)"
                like = f"%{filtro_q}%"
                parametros.extend([like, like, like, like])

            if filtro_rol in ["administrador", "tecnico", "cliente"]:
                consulta += " AND rol = %s"
                parametros.append(filtro_rol)

            consulta += " ORDER BY id DESC"
            usuarios = ejecutar_consulta(consulta, tuple(parametros), varias_filas=True)
        except Error:
            usuarios = []
            flash("No fue posible cargar usuarios desde base de datos.", "error")

        return render_template(
            "admin_usuarios.html",
            titulo_panel="INTC Admin",
            usuarios=usuarios,
            filtro_q=filtro_q,
            filtro_rol=filtro_rol,
        )

    @app.route("/panel/tecnico")
    def tecnico_dashboard():
        if not requiere_sesion() or not requiere_rol("tecnico", "administrador"):
            flash("No tienes permisos para acceder a este panel.", "error")
            return redirect(url_for("login"))

        tickets = obtener_tickets_usuario()
        solicitudes_pendientes = sum(1 for ticket in tickets if ticket.get("estado") == "Pendiente")
        en_proceso = sum(1 for ticket in tickets if ticket.get("estado") in ESTADOS_ORDEN_ACTIVA)
        listos = sum(1 for ticket in tickets if ticket.get("estado") == "Finalizado")

        return render_template(
            "gestor_dashboard.html",
            tickets=tickets,
            total_tickets=len(tickets),
            solicitudes_pendientes=solicitudes_pendientes,
            tickets_en_proceso=en_proceso,
            tickets_listos=listos,
            titulo_panel="INTC Técnico",
        )

    @app.route("/panel/gestor")
    def gestor_dashboard_legacy():
        return redirect(url_for("tecnico_dashboard"))

    @app.route("/panel/tickets")
    def tickets():
        if not requiere_sesion():
            return redirect(url_for("login"))

        tickets = obtener_tickets_usuario()
        solicitudes = [item for item in tickets if es_solicitud_ticket(item)]
        ordenes_activas = [item for item in tickets if es_orden_activa(item)]
        trabajos_finalizados = [item for item in tickets if es_trabajo_finalizado(item)]
        return render_template(
            "tickets.html",
            tickets=tickets,
            solicitudes=solicitudes,
            ordenes_activas=ordenes_activas,
            trabajos_finalizados=trabajos_finalizados,
            estados_ticket=ESTADOS_TICKET,
            estados_solicitud=ESTADOS_SOLICITUD,
            estados_orden_activa=ESTADOS_ORDEN_ACTIVA,
            estados_orden_cerrada=ESTADOS_ORDEN_CERRADA,
            titulo_panel="INTC Seguimiento",
        )

    @app.route("/panel/tickets/eliminar", methods=["POST"])
    def eliminar_ticket():
        if not requiere_sesion() or not requiere_rol("administrador", "tecnico"):
            flash("No tienes permisos para eliminar tickets.", "error")
            return redirect(url_for("login"))

        id_ticket = limpiar_texto(request.form.get("id_ticket"))
        if not id_ticket.isdigit():
            flash("Ticket inválido para eliminación.", "error")
            return redirect(url_for("tickets"))

        try:
            ticket = ejecutar_consulta("SELECT id FROM tickets WHERE id = %s", (int(id_ticket),), una_fila=True)
            if not ticket:
                flash("El ticket no existe.", "error")
                return redirect(url_for("tickets"))

            ejecutar_consulta("DELETE FROM ticket_mensajes WHERE id_ticket = %s", (int(id_ticket),), confirmar=True)
            ejecutar_consulta("DELETE FROM tickets WHERE id = %s", (int(id_ticket),), confirmar=True)
            flash("Ticket eliminado correctamente.", "exito")
        except Error:
            flash("No fue posible eliminar el ticket.", "error")

        return redirect(url_for("tickets"))

    @app.route("/panel/tickets/convertir-orden", methods=["POST"])
    def convertir_solicitud_orden():
        if not requiere_sesion() or not requiere_rol("administrador"):
            flash("No tienes permisos para convertir solicitudes en órdenes.", "error")
            return redirect(url_for("login"))

        id_ticket = limpiar_texto(request.form.get("id_ticket"))
        if not id_ticket.isdigit():
            flash("Solicitud inválida para conversión.", "error")
            return redirect(url_for("tickets"))

        ok, mensaje = convertir_ticket_a_orden(int(id_ticket), session.get("usuario_id"))
        flash(mensaje, "exito" if ok else "error")
        return redirect(url_for("tickets"))

    @app.route("/tickets")
    def tickets_public_alias():
        return redirect(url_for("tickets"))

    @app.route("/panel/contactos", methods=["GET", "POST"])
    def panel_contactos():
        acceso = verificar_acceso_operativo()
        if acceso:
            return acceso

        if request.method == "POST":
            id_contacto = limpiar_texto(request.form.get("id_contacto"))
            atendido = limpiar_texto(request.form.get("atendido"))

            if not id_contacto.isdigit() or atendido not in ["0", "1"]:
                flash("Datos inválidos para actualizar mensaje.", "error")
                return redirect(url_for("panel_contactos"))

            try:
                ejecutar_consulta(
                    "UPDATE contactos SET atendido = %s WHERE id = %s",
                    (int(atendido), int(id_contacto)),
                    confirmar=True,
                )
                flash("Estado del mensaje actualizado.", "exito")
            except Error:
                flash("No fue posible actualizar el mensaje.", "error")

            return redirect(url_for("panel_contactos"))

        try:
            mensajes = ejecutar_consulta(
                """
                SELECT id, nombre, correo, mensaje, atendido,
                       DATE_FORMAT(fecha_creacion, '%d/%m/%Y %H:%i') AS fecha
                FROM contactos
                ORDER BY atendido ASC, id DESC
                """,
                varias_filas=True,
            )
            chats = ejecutar_consulta(
                """
                SELECT t.id AS id_ticket, t.folio, t.estado,
                       CONCAT(u.nombres, ' ', u.apellidos) AS cliente,
                       DATE_FORMAT(MAX(tm.fecha_creacion), '%d/%m/%Y %H:%i') AS ultima_interaccion,
                       COUNT(tm.id) AS total_mensajes
                FROM tickets t
                INNER JOIN usuarios u ON u.id = t.id_usuario
                LEFT JOIN ticket_mensajes tm ON tm.id_ticket = t.id
                GROUP BY t.id, t.folio, t.estado, cliente
                ORDER BY t.id DESC
                """,
                varias_filas=True,
            )
        except Error:
            mensajes = []
            chats = []
            flash("No fue posible cargar la bandeja de mensajes.", "error")

        return render_template(
            "panel_contactos.html",
            mensajes=mensajes,
            chats=chats,
            titulo_panel="INTC Contactos",
        )

    @app.route("/panel/mensajes")
    def panel_mensajes():
        if not requiere_sesion():
            return redirect(url_for("login"))

        try:
            if requiere_rol("administrador", "tecnico"):
                chats = ejecutar_consulta(
                    """
                    SELECT t.id AS id_ticket, t.folio, t.estado,
                           CONCAT(u.nombres, ' ', u.apellidos) AS cliente,
                           DATE_FORMAT(MAX(tm.fecha_creacion), '%d/%m/%Y %H:%i') AS ultima_interaccion,
                           COUNT(tm.id) AS total_mensajes
                    FROM tickets t
                    INNER JOIN usuarios u ON u.id = t.id_usuario
                    LEFT JOIN ticket_mensajes tm ON tm.id_ticket = t.id
                    GROUP BY t.id, t.folio, t.estado, cliente
                    ORDER BY t.id DESC
                    """,
                    varias_filas=True,
                )
            else:
                chats = ejecutar_consulta(
                    """
                    SELECT t.id AS id_ticket, t.folio, t.estado,
                           'Soporte técnico' AS cliente,
                           DATE_FORMAT(MAX(tm.fecha_creacion), '%d/%m/%Y %H:%i') AS ultima_interaccion,
                           COUNT(tm.id) AS total_mensajes
                    FROM tickets t
                    LEFT JOIN ticket_mensajes tm ON tm.id_ticket = t.id
                    WHERE t.id_usuario = %s
                    GROUP BY t.id, t.folio, t.estado
                    ORDER BY t.id DESC
                    """,
                    (session.get("usuario_id"),),
                    varias_filas=True,
                )
        except Error:
            chats = []
            flash("No fue posible cargar la bandeja de chats.", "error")

        return render_template(
            "panel_mensajes.html",
            chats=chats,
            titulo_panel="INTC Mensajes",
        )

    @app.route("/panel/tickets/<int:id_ticket>")
    def ticket_detalle(id_ticket):
        if not requiere_sesion():
            return redirect(url_for("login"))

        ticket = obtener_ticket_por_id(id_ticket)

        if not ticket:
            flash("No se encontró el ticket solicitado o no tienes permisos para verlo.", "error")
            return redirect(url_for("tickets"))

        ticket["clase_estado"] = estado_a_clase(ticket["estado"])
        ticket["es_solicitud"] = es_solicitud_ticket(ticket)
        ticket["es_orden_activa"] = es_orden_activa(ticket)
        ticket["es_trabajo_finalizado"] = es_trabajo_finalizado(ticket)
        if ticket.get("detalle_precio_estimado"):
            ticket["precio_estimado_mostrar"] = ticket["detalle_precio_estimado"]
        elif ticket.get("precio_estimado_referencial") is not None:
            ticket["precio_estimado_mostrar"] = f"${float(ticket['precio_estimado_referencial']):.2f} MXN"
        else:
            ticket["precio_estimado_mostrar"] = "Pendiente de diagnóstico"

        mensajes_chat = obtener_mensajes_ticket(ticket["id"])
        historial_estado = obtener_historial_ticket(ticket["id"])

        return render_template(
            "ticket_detalle.html",
            ticket=ticket,
            mensajes_chat=mensajes_chat,
            historial_estado=historial_estado,
            titulo_panel="INTC Seguimiento",
        )

    @app.route("/panel/tickets/<int:id_ticket>/mensaje", methods=["POST"])
    def enviar_mensaje_ticket(id_ticket):
        if not requiere_sesion():
            return redirect(url_for("login"))

        ticket = obtener_ticket_por_id(id_ticket)
        if not ticket:
            flash("No tienes permisos para enviar mensajes a este ticket.", "error")
            return redirect(url_for("tickets"))

        mensaje = limpiar_texto(request.form.get("mensaje"))
        ok, error = validar_texto_seguro(mensaje, "mensaje", 2, 1200)
        if not ok:
            flash(error, "error")
            return redirect(url_for("ticket_detalle", id_ticket=id_ticket))

        try:
            ejecutar_consulta(
                "INSERT INTO ticket_mensajes (id_ticket, id_usuario, mensaje) VALUES (%s, %s, %s)",
                (id_ticket, session.get("usuario_id"), mensaje),
                confirmar=True,
            )
            flash("Mensaje enviado correctamente.", "exito")
        except Error:
            flash("No fue posible enviar el mensaje.", "error")

        return redirect(url_for("ticket_detalle", id_ticket=id_ticket))

    @app.route("/panel/tickets/estado", methods=["POST"])
    def actualizar_estado_ticket():
        if not requiere_sesion() or not requiere_rol("administrador", "tecnico"):
            flash("No tienes permisos para actualizar tickets.", "error")
            return redirect(url_for("login"))

        id_ticket = limpiar_texto(request.form.get("id_ticket"))
        nuevo_estado = limpiar_texto(request.form.get("nuevo_estado"))

        if not id_ticket.isdigit():
            flash("Identificador de ticket inválido.", "error")
            return redirect(url_for("tickets"))

        ok, mensaje = cambiar_estado_ticket(
            int(id_ticket),
            nuevo_estado,
            session.get("usuario_id"),
            "Cambio de estado desde panel operativo.",
        )
        flash(mensaje, "exito" if ok else "error")

        return redirect(url_for("tickets"))
