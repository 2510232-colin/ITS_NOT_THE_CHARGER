import re

from flask import flash, redirect, session, url_for
from mysql.connector import Error

from db import ejecutar_consulta


NEGOCIO = {
    "nombre": "PcCure",
    "ciudad": "Querétaro, Querétaro",
    "descripcion_corta": "Servicio técnico premium y tienda tecnológica",
}

ESTADOS_TICKET = [
    "Recibido",
    "En revisión",
    "En proceso",
    "Listo para recoger",
    "Entregado",
]

ESTADOS_PEDIDO = ["Pendiente", "En preparación", "Listo para recoger", "Entregado"]

POLITICA_DOMICILIO = [
    "La visita a domicilio está sujeta a cobertura por zona dentro de Querétaro.",
    "Puede aplicar recargo de traslado según distancia y horario.",
    "El diagnóstico en domicilio es referencial; la cotización final puede cambiar tras revisión técnica.",
    "Si el equipo requiere intervención mayor, se podrá solicitar ingreso en sucursal.",
]

MAPA_INTENCIONES = {
    "lenta": ["rendimiento", "optimizacion", "optimización", "ssd", "ram", "disco", "mantenimiento"],
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
        "Recibido": "revision",
        "En revisión": "revision",
        "En proceso": "proceso",
        "Listo para recoger": "listo",
        "Entregado": "listo",
    }
    return mapa.get(estado, "revision")


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


def recomendar_servicios_por_palabras(texto, servicios_catalogo, limite=5):
    palabras = normalizar_palabras(texto)
    if not palabras:
        return []

    palabras_ext = expandir_intenciones(palabras)

    resultados = []
    for servicio in servicios_catalogo:
        titulo = (servicio.get("titulo") or servicio.get("nombre") or "").lower()
        descripcion = (servicio.get("descripcion") or "").lower()
        categoria = (servicio.get("categoria") or "").lower()
        palabras_servicio = set(normalizar_palabras(servicio.get("palabras_clave") or "", max_palabras=80))
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

        if puntuacion > 0:
            resultados.append((puntuacion, servicio))

    resultados.sort(key=lambda item: (item[0], item[1].get("titulo") or item[1].get("nombre") or ""), reverse=True)
    return [item[1] for item in resultados[:limite]]


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
    fila = ejecutar_consulta("SELECT COUNT(*) AS total FROM tickets", una_fila=True)
    total = fila["total"] if fila else 0
    return f"TK-{1000 + total + 1}"


def obtener_tickets_usuario():
    if requiere_rol("administrador", "tecnico"):
        filas = ejecutar_consulta(
            """
            SELECT t.id AS id_ticket, t.folio, t.servicio_solicitado AS servicio, t.equipo, t.descripcion,
                   t.precio_estimado_referencial, t.detalle_precio_estimado, t.acepta_politica_domicilio,
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
