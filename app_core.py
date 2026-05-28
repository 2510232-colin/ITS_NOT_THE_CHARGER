import re
import os

from flask import flash, redirect, session, url_for
from mysql.connector import Error

from ai_disambiguator import desempatar_servicio_con_gemini
from db import ejecutar_consulta


NEGOCIO = {
    "nombre": "IT'S NOT THE CHARGER",
    "ciudad": "Querétaro, Querétaro",
    "descripcion_corta": "Servicio técnico premium y tienda tecnológica",
}

ESTADOS_TICKET = [
    "Pendiente",
    "Validado",
    "Agendado",
    "En diagnóstico",
    "Esperando aprobación",
    "En reparación",
    "Finalizado",
    "Entregado",
    "Cancelado",
]

ESTADOS_SOLICITUD = [
    "Pendiente",
    "Validado",
    "Agendado",
    "Cancelado",
]

ESTADOS_ORDEN_ACTIVA = [
    "En diagnóstico",
    "Esperando aprobación",
    "En reparación",
]

ESTADOS_ORDEN_CERRADA = [
    "Finalizado",
    "Entregado",
]

TRANSICIONES_SOLICITUD = {
    "Pendiente": {"Validado", "Agendado", "Cancelado"},
    "Validado": {"Agendado", "Cancelado"},
    "Agendado": {"Validado", "Cancelado"},
    "Cancelado": set(),
}

TRANSICIONES_ORDEN = {
    "En diagnóstico": {"Esperando aprobación", "En reparación", "Cancelado"},
    "Esperando aprobación": {"En reparación", "Cancelado"},
    "En reparación": {"Finalizado", "Cancelado"},
    "Finalizado": {"Entregado"},
    "Entregado": set(),
    "Cancelado": set(),
}

ESTADOS_PEDIDO = ["Pendiente", "En preparación", "Listo para recoger", "Entregado"]

POLITICA_DOMICILIO = [
    "La visita a domicilio está sujeta a cobertura por zona dentro de Querétaro.",
    "Puede aplicar recargo de traslado según distancia y horario.",
    "El diagnóstico en domicilio es referencial; la cotización final puede cambiar tras revisión técnica.",
    "Si el equipo requiere intervención mayor, se podrá solicitar ingreso en sucursal.",
]

MAPA_INTENCIONES = {
    "lenta": ["rendimiento", "optimizacion", "optimización", "ssd", "ram", "disco", "mantenimiento"],
    "lento": ["rendimiento", "optimizacion", "optimización", "ssd", "ram", "disco", "mantenimiento"],
    "lentitud": ["rendimiento", "optimizacion", "optimización", "ssd", "ram", "disco", "mantenimiento"],
    "calienta": ["sobrecalentamiento", "pasta termica", "pasta térmica", "ventilador", "limpieza"],
    "sobrecalienta": ["sobrecalentamiento", "pasta termica", "pasta térmica", "ventilador", "limpieza"],
    "enciende": ["fuente", "energía", "diagnostico", "diagnóstico", "placa"],
    "pantalla": ["display", "panel", "video", "gpu", "grafica", "gráfica"],
    "virus": ["malware", "seguridad", "limpieza", "formateo"],
    "arranque": ["sistema", "ssd", "formateo", "optimización", "optimizacion"],
    "gamer": ["ram", "ssd", "gpu", "optimización", "optimizacion"],
    "trabajo": ["mantenimiento", "respaldo", "productividad", "optimización", "optimizacion"],
}


def estado_a_clase(estado):
    mapa = {
        "Pendiente": "revision",
        "Validado": "revision",
        "Agendado": "revision",
        "En diagnóstico": "proceso",
        "Esperando aprobación": "proceso",
        "En reparación": "proceso",
        "Finalizado": "listo",
        "Entregado": "listo",
        "Cancelado": "cancelado",
    }
    return mapa.get(estado, "revision")


def es_estado_valido_ticket(estado):
    return estado in ESTADOS_TICKET


def es_solicitud_ticket(ticket):
    return not bool(ticket.get("es_orden_trabajo"))


def es_orden_activa(ticket):
    return bool(ticket.get("es_orden_trabajo")) and ticket.get("estado") in ESTADOS_ORDEN_ACTIVA


def es_trabajo_finalizado(ticket):
    return ticket.get("estado") in ESTADOS_ORDEN_CERRADA


def construir_etiqueta_precio(servicio):
    tipo = servicio.get("tipo_precio", "fijo")
    precio = servicio.get("precio") or 0
    precio_min = servicio.get("precio_min")
    precio_max = servicio.get("precio_max")

    if tipo == "desde":
        return f"Desde ${float(precio):.2f} MXN"
    if tipo == "rango" and precio_min is not None and precio_max is not None:
        return f"${float(precio_min):.2f} a ${float(precio_max):.2f} MXN"
    if tipo == "recargo":
        return f"+${float(precio):.2f} MXN"
    return f"${float(precio):.2f} MXN"


def enriquecer_servicios(servicios):
    for servicio in servicios:
        servicio["precio_mostrar"] = construir_etiqueta_precio(servicio)
    return servicios


def normalizar_palabras(texto, max_palabras=12):
    tokens = re.findall(r"[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ0-9]+", (texto or "").lower())
    tokens = [token for token in tokens if len(token) >= 3]
    return tokens[:max_palabras]


def expandir_intenciones(tokens):
    resultado = set(tokens)
    for token in tokens:
        for clave, palabras in MAPA_INTENCIONES.items():
            if clave in token or token in clave:
                resultado.update(normalizar_palabras(" ".join(palabras), max_palabras=50))
    return list(resultado)


def recomendar_servicios_por_palabras_con_puntaje(texto, servicios_catalogo, limite=5):
    palabras = normalizar_palabras(texto)
    if not palabras:
        return []

    palabras_ext = expandir_intenciones(palabras)
    texto_normalizado = " ".join(palabras)
    intención_lentitud = any(token in texto_normalizado for token in ["lenta", "lento", "lentitud", "arranque", "arranca"])
    intención_seguridad = any(token in texto_normalizado for token in ["virus", "malware", "spyware", "seguridad"])
    intención_termica = any(token in texto_normalizado for token in ["calienta", "sobrecal", "temperatura", "ventilador"])
    intención_armado = any(token in texto_normalizado for token in ["armar", "armado", "ensamble", "nueva pc", "pc nueva", "gamer"])

    resultados = []
    for servicio in servicios_catalogo:
        titulo = (servicio.get("titulo") or servicio.get("nombre") or "").lower()
        descripcion = (servicio.get("descripcion") or "").lower()
        categoria = (servicio.get("categoria") or "").lower()
        palabras_servicio = set(normalizar_palabras(servicio.get("palabras_clave") or "", max_palabras=80))
        texto_servicio = " ".join([titulo, descripcion, categoria, " ".join(palabras_servicio)])
        puntuacion = 0

        for palabra in palabras_ext:
            if palabra in titulo:
                puntuacion += 5
            if palabra in categoria:
                puntuacion += 3
            if palabra in descripcion:
                puntuacion += 2
            if palabra in palabras_servicio:
                puntuacion += 7

        if intención_lentitud:
            if any(token in texto_servicio for token in ["ssd", "nvme", "migración", "migracion", "hdd"]):
                puntuacion += 18
            if any(token in texto_servicio for token in ["ram", "memoria"]):
                puntuacion += 10
            if any(token in texto_servicio for token in ["upgrade", "actualización", "actualizacion", "ensamblaje"]):
                puntuacion += 8

            es_upgrade = "upgrade y ensamblaje" in categoria
            es_ssd_ram_especifico = any(
                token in titulo
                for token in [
                    "instalación de ssd",
                    "instalacion de ssd",
                    "migración de hdd a ssd",
                    "migracion de hdd a ssd",
                    "actualización de memoria ram",
                    "actualizacion de memoria ram",
                    "upgrade completo",
                ]
            )

            if es_ssd_ram_especifico:
                puntuacion += 35
            elif es_upgrade:
                puntuacion += 22

            if not intención_seguridad and "seguridad y optimización" in categoria:
                puntuacion -= 10
            if not intención_termica and "mantenimiento preventivo y correctivo" in categoria:
                puntuacion -= 8
            if not intención_armado and any(token in titulo for token in ["armado", "ensamble", "personalizada"]):
                puntuacion -= 26

        if intención_armado:
            if any(token in texto_servicio for token in ["armado", "ensamble", "personalizada", "gamer", "upgrade y ensamblaje"]):
                puntuacion += 28
            if "gamer" in texto_normalizado and "gamer" in titulo:
                puntuacion += 14
            if "seguridad y optimización" in categoria and "gamer" not in titulo:
                puntuacion -= 12

        if puntuacion > 0:
            resultados.append({"score": puntuacion, "servicio": servicio})

    resultados.sort(
        key=lambda item: (item["score"], item["servicio"].get("titulo") or item["servicio"].get("nombre") or ""),
        reverse=True,
    )
    return resultados[:limite]


def recomendar_servicios_por_palabras(texto, servicios_catalogo, limite=5):
    resultados = recomendar_servicios_por_palabras_con_puntaje(texto, servicios_catalogo, limite=limite)
    return [item["servicio"] for item in resultados]


def resolver_recomendacion_servicios_ui(texto, servicios_catalogo, limite=4):
    resultados = recomendar_servicios_por_palabras_con_puntaje(texto, servicios_catalogo, limite=max(5, limite))

    salida_base = {
        "modo": "low",
        "recomendaciones": [],
        "principal": None,
        "comparables": [],
        "sugerido_id": None,
        "sugerencias_contexto": [
            "¿Tu equipo muestra algún mensaje de error?",
            "¿Es laptop o PC de escritorio?",
            "¿El problema ocurre al encender o durante el uso?",
        ],
    }

    if not resultados:
        return salida_base

    recomendaciones = [item["servicio"] for item in resultados[:limite]]
    top1 = resultados[0]["score"]
    top2 = resultados[1]["score"] if len(resultados) > 1 else 0
    diferencia = top1 - top2

    if top1 < 8:
        salida_base["recomendaciones"] = recomendaciones
        return salida_base

    gemini_enabled = (os.getenv("USE_GEMINI_DISAMBIGUATION") or "false").strip().lower() in {"1", "true", "yes", "on"}
    ambiguo = len(resultados) > 1 and (top1 == top2 or diferencia <= 2 or top1 < 14)

    if ambiguo:
        sugerido_id = None
        if gemini_enabled:
            candidatos = []
            for item in resultados[:5]:
                servicio = item["servicio"]
                candidatos.append(
                    {
                        "id": servicio.get("id"),
                        "nombre": servicio.get("titulo") or servicio.get("nombre") or "",
                        "categoria": servicio.get("categoria") or "",
                        "descripcion": servicio.get("descripcion") or "",
                        "palabras_clave": servicio.get("palabras_clave") or "",
                        "score_heuristico": item["score"],
                    }
                )
            sugerido_id = desempatar_servicio_con_gemini(texto, candidatos)

        comparables = [item["servicio"] for item in resultados[:3]]
        salida_base.update(
            {
                "modo": "ambiguo",
                "recomendaciones": recomendaciones,
                "comparables": comparables,
                "sugerido_id": sugerido_id,
            }
        )
        return salida_base

    salida_base.update(
        {
            "modo": "alta",
            "recomendaciones": recomendaciones,
            "principal": resultados[0]["servicio"],
        }
    )
    return salida_base


def calcular_estimado_referencial(servicio):
    tipo = servicio.get("tipo_precio", "fijo")
    precio = float(servicio.get("precio") or 0)
    precio_min = servicio.get("precio_min")
    precio_max = servicio.get("precio_max")

    if tipo == "rango" and precio_min is not None and precio_max is not None:
        precio_min_valor = float(precio_min)
        precio_max_valor = float(precio_max)
        promedio = round((precio_min_valor + precio_max_valor) / 2, 2)
        detalle = f"Rango estimado: ${precio_min_valor:.2f} a ${precio_max_valor:.2f} MXN"
        return promedio, detalle
    if tipo == "desde":
        detalle = f"Desde ${precio:.2f} MXN"
        return precio, detalle
    if tipo == "recargo":
        detalle = f"Recargo estimado de +${precio:.2f} MXN"
        return precio, detalle

    detalle = f"${precio:.2f} MXN"
    return precio, detalle


def normalizar_rol(rol):
    if rol == "gestor":
        return "tecnico"
    return rol


def estimar_ticket_por_texto(servicio_requerido, equipo, descripcion_problema):
    texto_busqueda = " ".join([servicio_requerido or "", equipo or "", descripcion_problema or ""]).strip()
    if not texto_busqueda:
        return None, "Pendiente de diagnóstico en sucursal"

    try:
        servicios_catalogo = ejecutar_consulta(
            """
            SELECT id, categoria, nombre AS titulo, descripcion, tipo_precio, precio, precio_min, precio_max, palabras_clave
            FROM servicios
            WHERE activo = 1
            """,
            varias_filas=True,
        )
    except Error:
        return None, "Pendiente de diagnóstico en sucursal"

    recomendados = recomendar_servicios_por_palabras(texto_busqueda, servicios_catalogo, limite=1)
    if not recomendados:
        return None, "Pendiente de diagnóstico en sucursal"

    servicio_base = recomendados[0]
    estimado, etiqueta = calcular_estimado_referencial(servicio_base)
    detalle = f"{etiqueta} · Basado en: {servicio_base.get('titulo', 'Servicio relacionado')}"
    return estimado, detalle


def slug_categoria(nombre):
    base = (nombre or "").strip().lower()
    base = re.sub(r"[^a-z0-9áéíóúüñ\s-]", "", base)
    base = re.sub(r"\s+", "-", base)
    return base


def obtener_categorias_servicios():
    filas = ejecutar_consulta(
        """
        SELECT categoria, COUNT(*) AS total
        FROM servicios
        WHERE activo = 1
        GROUP BY categoria
        ORDER BY categoria ASC
        """,
        varias_filas=True,
    )
    for fila in filas:
        fila["slug"] = slug_categoria(fila["categoria"])
    return filas


def obtener_contenido_sitio():
    contenido = {
        "titulo_hero": "Servicio técnico premium para tu equipo",
        "subtitulo_hero": "Atención ordenada, rápida y con estilo tecnológico.",
        "mensaje_promocional": "Promociones semanales disponibles en sucursal.",
    }
    try:
        fila = ejecutar_consulta(
            """
            SELECT titulo_hero, subtitulo_hero, mensaje_promocional
            FROM contenido_sitio
            WHERE id = 1
            LIMIT 1
            """,
            una_fila=True,
        )
        if fila:
            contenido.update(fila)
    except Error:
        return contenido
    return contenido


def requiere_sesion():
    return bool(session.get("usuario_id"))


def requiere_rol(*roles):
    rol_actual = normalizar_rol(session.get("rol"))
    return rol_actual in roles


def redireccion_por_rol(rol):
    rol = normalizar_rol(rol)
    if rol == "administrador":
        return url_for("admin_dashboard")
    if rol == "tecnico":
        return url_for("tecnico_dashboard")
    return url_for("cliente_dashboard")


def verificar_acceso_admin():
    if not requiere_sesion() or not requiere_rol("administrador"):
        flash("No tienes permisos para acceder al panel de administración.", "error")
        return redirect(url_for("login"))
    return None


def verificar_acceso_operativo():
    if not requiere_sesion() or not requiere_rol("administrador", "tecnico"):
        flash("No tienes permisos para acceder a este módulo.", "error")
        return redirect(url_for("login"))
    return None


def generar_folio_ticket():
    fila = ejecutar_consulta("SELECT MAX(id) AS ultimo_id FROM tickets", una_fila=True)
    ultimo_id = int(fila["ultimo_id"] or 0) if fila else 0
    return f"TK-{1000 + ultimo_id + 1}"


def obtener_tickets_usuario():
    if requiere_rol("administrador", "tecnico"):
        filas = ejecutar_consulta(
            """
            SELECT t.id AS id_ticket, t.folio, t.servicio_solicitado AS servicio, t.equipo, t.descripcion,
                   t.precio_estimado_referencial, t.detalle_precio_estimado, t.acepta_politica_domicilio,
                     t.modalidad_atencion, t.notas_adicionales, t.es_orden_trabajo,
                     DATE_FORMAT(t.fecha_creacion, '%d/%m/%Y') AS fecha, t.estado
            FROM tickets t
            ORDER BY t.id DESC
            """,
            varias_filas=True,
        )
    else:
        filas = ejecutar_consulta(
            """
            SELECT t.id AS id_ticket, t.folio, t.servicio_solicitado AS servicio, t.equipo, t.descripcion,
                   t.precio_estimado_referencial, t.detalle_precio_estimado, t.acepta_politica_domicilio,
                     t.modalidad_atencion, t.notas_adicionales, t.es_orden_trabajo,
                     DATE_FORMAT(t.fecha_creacion, '%d/%m/%Y') AS fecha, t.estado
            FROM tickets t
            WHERE t.id_usuario = %s
            ORDER BY t.id DESC
            """,
            (session.get("usuario_id"),),
            varias_filas=True,
        )

    for fila in filas:
        fila["clase_estado"] = estado_a_clase(fila["estado"])
        if fila.get("precio_estimado_referencial") is not None:
            fila["precio_estimado_lista"] = f"${float(fila['precio_estimado_referencial']):.2f} MXN"
        else:
            fila["precio_estimado_lista"] = "Pendiente"

        if fila.get("detalle_precio_estimado"):
            fila["precio_estimado_mostrar"] = fila["detalle_precio_estimado"]
        elif fila.get("precio_estimado_referencial") is not None:
            fila["precio_estimado_mostrar"] = f"${float(fila['precio_estimado_referencial']):.2f} MXN"
        else:
            fila["precio_estimado_mostrar"] = "Pendiente de diagnóstico"

        fila["es_solicitud"] = es_solicitud_ticket(fila)
        fila["es_orden_activa"] = es_orden_activa(fila)
        fila["es_trabajo_finalizado"] = es_trabajo_finalizado(fila)

    return filas


def obtener_ticket_por_id(id_ticket):
    parametros = [id_ticket]
    condicion_permiso = ""
    if not requiere_rol("administrador", "tecnico"):
        condicion_permiso = " AND t.id_usuario = %s"
        parametros.append(session.get("usuario_id"))

    try:
        return ejecutar_consulta(
            f"""
            SELECT t.id, t.folio, t.id_usuario, t.servicio_solicitado, t.equipo, t.descripcion, t.estado,
                   t.precio_estimado_referencial, t.detalle_precio_estimado, t.acepta_politica_domicilio,
                     t.modalidad_atencion, t.notas_adicionales, t.es_orden_trabajo,
                   DATE_FORMAT(t.fecha_creacion, '%d/%m/%Y %H:%i') AS fecha,
                   CONCAT(u.nombres, ' ', u.apellidos) AS cliente
            FROM tickets t
            INNER JOIN usuarios u ON u.id = t.id_usuario
            WHERE t.id = %s{condicion_permiso}
            LIMIT 1
            """,
            tuple(parametros),
            una_fila=True,
        )
    except Error:
        return None


def obtener_mensajes_ticket(id_ticket):
    try:
        return ejecutar_consulta(
            """
            SELECT tm.id, tm.id_usuario, tm.mensaje, DATE_FORMAT(tm.fecha_creacion, '%d/%m/%Y %H:%i') AS fecha,
                   u.nombres, u.rol
            FROM ticket_mensajes tm
            INNER JOIN usuarios u ON u.id = tm.id_usuario
            WHERE tm.id_ticket = %s
            ORDER BY tm.id ASC
            """,
            (id_ticket,),
            varias_filas=True,
        )
    except Error:
        return []


def obtener_historial_ticket(id_ticket):
    try:
        return ejecutar_consulta(
            """
            SELECT h.id, h.estado_anterior, h.estado_nuevo, h.comentario,
                   DATE_FORMAT(h.fecha_creacion, '%d/%m/%Y %H:%i') AS fecha,
                   COALESCE(u.nombres, 'Sistema') AS actor,
                   COALESCE(u.rol, 'sistema') AS actor_rol
            FROM ticket_historial h
            LEFT JOIN usuarios u ON u.id = h.id_usuario
            WHERE h.id_ticket = %s
            ORDER BY h.id DESC
            """,
            (id_ticket,),
            varias_filas=True,
        )
    except Error:
        return []


def registrar_historial_ticket(id_ticket, estado_anterior, estado_nuevo, id_usuario=None, comentario=""):
    try:
        ejecutar_consulta(
            """
            INSERT INTO ticket_historial (id_ticket, estado_anterior, estado_nuevo, id_usuario, comentario)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (id_ticket, estado_anterior, estado_nuevo, id_usuario, (comentario or "")[:500]),
            confirmar=True,
        )
    except Error:
        return False
    return True


def cambiar_estado_ticket(id_ticket, nuevo_estado, id_usuario=None, comentario=""):
    if not es_estado_valido_ticket(nuevo_estado):
        return False, "Estado de ticket inválido."

    try:
        ticket = ejecutar_consulta(
            "SELECT id, estado, es_orden_trabajo FROM tickets WHERE id = %s LIMIT 1",
            (id_ticket,),
            una_fila=True,
        )
        if not ticket:
            return False, "El ticket seleccionado no existe."

        estado_anterior = ticket.get("estado")
        if estado_anterior == nuevo_estado:
            return True, "Sin cambios: el ticket ya está en ese estado."

        es_orden = bool(ticket.get("es_orden_trabajo"))
        if es_orden:
            if nuevo_estado not in TRANSICIONES_ORDEN:
                return False, "Estado inválido para una orden de trabajo."
            permitidos = TRANSICIONES_ORDEN.get(estado_anterior, set())
            if nuevo_estado not in permitidos:
                return False, f"Transición no permitida de '{estado_anterior}' a '{nuevo_estado}'."
        else:
            if nuevo_estado not in TRANSICIONES_SOLICITUD:
                return False, "Estado inválido para una solicitud."
            permitidos = TRANSICIONES_SOLICITUD.get(estado_anterior, set())
            if nuevo_estado not in permitidos:
                return False, f"Transición no permitida de '{estado_anterior}' a '{nuevo_estado}'."

        ejecutar_consulta(
            "UPDATE tickets SET estado = %s WHERE id = %s",
            (nuevo_estado, id_ticket),
            confirmar=True,
        )
        registrar_historial_ticket(id_ticket, estado_anterior, nuevo_estado, id_usuario, comentario)
        return True, "Estado actualizado correctamente."
    except Error:
        return False, "No fue posible actualizar el estado del ticket."


def convertir_ticket_a_orden(id_ticket, id_usuario=None):
    try:
        ticket = ejecutar_consulta(
            "SELECT id, estado, es_orden_trabajo FROM tickets WHERE id = %s LIMIT 1",
            (id_ticket,),
            una_fila=True,
        )
        if not ticket:
            return False, "La solicitud indicada no existe."

        if ticket.get("es_orden_trabajo"):
            return False, "Este ticket ya fue convertido en orden de trabajo."

        if ticket.get("estado") not in {"Validado", "Agendado"}:
            return False, "Solo las solicitudes validadas o agendadas pueden convertirse en orden de trabajo."

        ejecutar_consulta(
            """
            UPDATE tickets
            SET es_orden_trabajo = 1,
                fecha_orden = NOW(),
                estado = 'En diagnóstico'
            WHERE id = %s
            """,
            (id_ticket,),
            confirmar=True,
        )

        registrar_historial_ticket(
            id_ticket,
            ticket.get("estado"),
            "En diagnóstico",
            id_usuario,
            "Solicitud convertida a orden de trabajo.",
        )
        return True, "Solicitud convertida en orden de trabajo correctamente."
    except Error:
        return False, "No fue posible convertir la solicitud en orden de trabajo."


def _columna_existe_tabla(tabla, columna):
    try:
        fila = ejecutar_consulta(
            """
            SELECT COUNT(*) AS total
            FROM information_schema.columns
            WHERE table_schema = DATABASE() AND table_name = %s AND column_name = %s
            """,
            (tabla, columna),
            una_fila=True,
        )
        return bool(fila and fila.get("total", 0) > 0)
    except Error:
        return False


def _indice_existe_tabla(tabla, indice):
    try:
        fila = ejecutar_consulta(
            """
            SELECT COUNT(*) AS total
            FROM information_schema.statistics
            WHERE table_schema = DATABASE() AND table_name = %s AND index_name = %s
            """,
            (tabla, indice),
            una_fila=True,
        )
        return bool(fila and fila.get("total", 0) > 0)
    except Error:
        return False


def asegurar_modelo_tickets():
    try:
        ejecutar_consulta(
            """
            CREATE TABLE IF NOT EXISTS ticket_historial (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_ticket INT NOT NULL,
                estado_anterior VARCHAR(60) NULL,
                estado_nuevo VARCHAR(60) NOT NULL,
                id_usuario INT NULL,
                comentario VARCHAR(500) NULL,
                fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_ticket) REFERENCES tickets(id) ON DELETE CASCADE,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE SET NULL
            )
            """,
            confirmar=True,
        )

        if not _columna_existe_tabla("tickets", "modalidad_atencion"):
            ejecutar_consulta(
                """
                ALTER TABLE tickets
                ADD COLUMN modalidad_atencion ENUM('domicilio', 'sucursal') NOT NULL DEFAULT 'sucursal'
                """,
                confirmar=True,
            )

        if not _columna_existe_tabla("tickets", "notas_adicionales"):
            ejecutar_consulta(
                "ALTER TABLE tickets ADD COLUMN notas_adicionales TEXT NULL",
                confirmar=True,
            )

        if not _columna_existe_tabla("tickets", "es_orden_trabajo"):
            ejecutar_consulta(
                "ALTER TABLE tickets ADD COLUMN es_orden_trabajo TINYINT(1) NOT NULL DEFAULT 0",
                confirmar=True,
            )

        if not _columna_existe_tabla("tickets", "fecha_orden"):
            ejecutar_consulta(
                "ALTER TABLE tickets ADD COLUMN fecha_orden DATETIME NULL",
                confirmar=True,
            )

        ejecutar_consulta("UPDATE tickets SET estado = 'Pendiente' WHERE estado = 'Recibido'", confirmar=True)
        ejecutar_consulta("UPDATE tickets SET estado = 'Validado' WHERE estado = 'En revisión'", confirmar=True)
        ejecutar_consulta("UPDATE tickets SET estado = 'En diagnóstico' WHERE estado = 'En proceso'", confirmar=True)
        ejecutar_consulta("UPDATE tickets SET estado = 'Finalizado' WHERE estado = 'Listo para recoger'", confirmar=True)

        ejecutar_consulta(
            """
            ALTER TABLE tickets
            MODIFY COLUMN estado ENUM(
                'Pendiente',
                'Validado',
                'Agendado',
                'En diagnóstico',
                'Esperando aprobación',
                'En reparación',
                'Finalizado',
                'Entregado',
                'Cancelado'
            ) NOT NULL DEFAULT 'Pendiente'
            """,
            confirmar=True,
        )
    except Error:
        return False
    return True


def asegurar_modelo_servicios():
    try:
        if not _columna_existe_tabla("servicios", "sintomas_comunes"):
            ejecutar_consulta(
                "ALTER TABLE servicios ADD COLUMN sintomas_comunes TEXT NULL",
                confirmar=True,
            )

        if not _columna_existe_tabla("servicios", "problemas_relacionados"):
            ejecutar_consulta(
                "ALTER TABLE servicios ADD COLUMN problemas_relacionados TEXT NULL",
                confirmar=True,
            )

        if not _columna_existe_tabla("servicios", "prioridad"):
            ejecutar_consulta(
                "ALTER TABLE servicios ADD COLUMN prioridad TINYINT UNSIGNED NOT NULL DEFAULT 3",
                confirmar=True,
            )

        if not _columna_existe_tabla("servicios", "promocion_tipo"):
            ejecutar_consulta(
                "ALTER TABLE servicios ADD COLUMN promocion_tipo VARCHAR(30) NULL",
                confirmar=True,
            )

        if not _columna_existe_tabla("servicios", "promocion_valor"):
            ejecutar_consulta(
                "ALTER TABLE servicios ADD COLUMN promocion_valor DECIMAL(10,2) NULL",
                confirmar=True,
            )

        if not _columna_existe_tabla("servicios", "promocion_detalle"):
            ejecutar_consulta(
                "ALTER TABLE servicios ADD COLUMN promocion_detalle VARCHAR(200) NULL",
                confirmar=True,
            )

        ejecutar_consulta(
            "UPDATE servicios SET prioridad = 3 WHERE prioridad IS NULL OR prioridad < 1 OR prioridad > 5",
            confirmar=True,
        )
    except Error:
        return False
    return True


def asegurar_modelo_auth_social():
    try:
        if not _columna_existe_tabla("usuarios", "firebase_uid"):
            ejecutar_consulta(
                "ALTER TABLE usuarios ADD COLUMN firebase_uid VARCHAR(128) NULL",
                confirmar=True,
            )

        if not _columna_existe_tabla("usuarios", "auth_provider"):
            ejecutar_consulta(
                "ALTER TABLE usuarios ADD COLUMN auth_provider VARCHAR(20) NULL",
                confirmar=True,
            )

        if not _indice_existe_tabla("usuarios", "idx_usuarios_firebase_uid"):
            ejecutar_consulta(
                "CREATE UNIQUE INDEX idx_usuarios_firebase_uid ON usuarios(firebase_uid)",
                confirmar=True,
            )
    except Error:
        return False
    return True


def construir_detalle_ampliado_servicio(servicio):
    titulo = (servicio.get("titulo") or "Servicio técnico").strip()
    descripcion = (servicio.get("descripcion") or "").strip()
    categoria = (servicio.get("categoria") or "General").strip()
    modalidad = (servicio.get("modalidad") or "sucursal").strip().lower()
    tiempo = servicio.get("tiempo_estimado") or "Por definir"
    requiere_diagnostico = bool(servicio.get("requiere_diagnostico"))

    texto_base = f"{titulo} {descripcion} {categoria}".lower()

    incluye = [
        "Recepción y revisión inicial del equipo para confirmar síntomas reportados.",
        "Ejecución técnica del servicio con pruebas de funcionamiento y estabilidad.",
        "Validación final antes de entrega para asegurar que el problema principal quede atendido.",
    ]

    if "limpieza" in texto_base or "mantenimiento" in texto_base:
        incluye.append("Limpieza física y verificación de temperatura/ruido cuando aplica.")
    if "instalación" in texto_base or "configuración" in texto_base:
        incluye.append("Ajustes de instalación y configuración inicial para dejar el servicio operativo.")
    if "virus" in texto_base or "malware" in texto_base or "seguridad" in texto_base:
        incluye.append("Revisión de seguridad básica posterior para reducir reincidencias.")
    if "respaldo" in texto_base or "migración" in texto_base:
        incluye.append("Validación de integridad de la información transferida o recuperada.")

    no_incluye = [
        "Refacciones o licencias de software de pago (se cotizan por separado).",
        "Daños adicionales no detectados en el diagnóstico inicial.",
        "Incidencias por uso posterior fuera de recomendaciones técnicas.",
    ]

    ideal_para = []
    if "sobrecal" in texto_base or "temperatura" in texto_base:
        ideal_para.append("Equipos que se calientan, se apagan solos o reducen rendimiento por temperatura.")
    if "lenta" in texto_base or "optim" in texto_base or "arranque" in texto_base:
        ideal_para.append("Equipos con lentitud general, arranque tardado o bajo rendimiento diario.")
    if "virus" in texto_base or "malware" in texto_base:
        ideal_para.append("Equipos con ventanas emergentes, comportamiento extraño o riesgo de seguridad.")
    if "ram" in texto_base or "ssd" in texto_base or "upgrade" in texto_base:
        ideal_para.append("Usuarios que necesitan mejorar rendimiento para estudio, trabajo o gaming.")
    if "red" in texto_base or "wifi" in texto_base or "router" in texto_base:
        ideal_para.append("Espacios con fallas de conectividad, cobertura o estabilidad de internet.")

    if not ideal_para:
        ideal_para.append("Usuarios que necesitan resolver el problema descrito con soporte técnico guiado.")

    recomendaciones = [
        f"Tiempo estimado de atención: {tiempo}.",
        "Respalda información importante antes del servicio cuando sea posible.",
        "Describe síntomas concretos (cuándo falla, frecuencia y mensajes de error) para mejorar precisión.",
    ]

    if requiere_diagnostico:
        recomendaciones.insert(0, "Este servicio requiere diagnóstico previo para definir alcance y costo final.")
    else:
        recomendaciones.insert(0, "Este servicio normalmente puede ejecutarse sin diagnóstico profundo adicional.")

    modalidad_texto = {
        "sucursal": "Atención en sucursal con entrega y recolección directa del equipo.",
        "domicilio": "Atención en domicilio sujeta a cobertura de zona y condiciones de traslado.",
        "remoto": "Atención remota mediante conexión asistida, ideal para ajustes de software.",
        "mixto": "Atención combinada: parte remota y parte en sucursal/domicilio según el caso.",
    }.get(modalidad, "Modalidad definida según evaluación técnica.")

    descripcion_larga = (
        f"{titulo} pertenece a la categoría "
        f"\"{categoria}\" y está diseñado para atender necesidades técnicas de forma controlada y verificable. "
        f"{descripcion} {modalidad_texto} "
        "Antes de cerrar el servicio, se realiza una validación final para confirmar estabilidad y funcionamiento."
    )

    return {
        "descripcion_larga": descripcion_larga,
        "incluye": incluye,
        "no_incluye": no_incluye,
        "ideal_para": ideal_para,
        "recomendaciones": recomendaciones,
    }
