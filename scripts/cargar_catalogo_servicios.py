from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from db import obtener_conexion


SERVICIOS = [
    # Reparación y diagnóstico
    ("Reparación y diagnóstico", "Diagnóstico general de computadora", "Evaluación inicial de equipo y detección de fallas.", "fijo", 200, None, None, 0, "sucursal", "Mismo día"),
    ("Reparación y diagnóstico", "Diagnóstico avanzado de hardware", "Pruebas detalladas para identificar componentes dañados.", "fijo", 350, None, None, 0, "sucursal", "1 día"),
    ("Reparación y diagnóstico", "Revisión de fallas de hardware", "Análisis físico y lógico de componentes críticos.", "fijo", 300, None, None, 0, "sucursal", "Mismo día"),
    ("Reparación y diagnóstico", "Reparación de PC de escritorio", "Corrección de fallas generales en PC de escritorio.", "desde", 800, None, None, 1, "sucursal", "1 a 3 días"),
    ("Reparación y diagnóstico", "Reparación de laptops", "Reparación de equipos portátiles por falla de hardware/software.", "desde", 900, None, None, 1, "sucursal", "1 a 4 días"),
    ("Reparación y diagnóstico", "Reparación de fuente de poder", "Diagnóstico y reparación o sustitución de fuente dañada.", "desde", 700, None, None, 1, "sucursal", "1 a 2 días"),
    ("Reparación y diagnóstico", "Reparación de tarjeta madre", "Diagnóstico y reparación de motherboard.", "desde", 1200, None, None, 1, "sucursal", "2 a 5 días"),
    ("Reparación y diagnóstico", "Solución de sobrecalentamiento", "Ajustes para reducir temperaturas y mejorar estabilidad.", "desde", 500, None, None, 0, "mixto", "Mismo día"),
    ("Reparación y diagnóstico", "Solución de pantallazo azul", "Corrección de errores críticos de Windows y controladores.", "fijo", 450, None, None, 0, "sucursal", "Mismo día"),
    ("Reparación y diagnóstico", "Problemas de encendido", "Diagnóstico y corrección de fallas de arranque eléctrico.", "desde", 600, None, None, 1, "sucursal", "1 a 3 días"),
    ("Reparación y diagnóstico", "Equipo lento / optimización profunda", "Limpieza y ajustes avanzados de rendimiento.", "fijo", 500, None, None, 0, "mixto", "Mismo día"),
    ("Reparación y diagnóstico", "Recuperación de equipo que no inicia", "Procedimientos para recuperar sistema y arranque.", "desde", 700, None, None, 1, "sucursal", "1 a 3 días"),
    ("Reparación y diagnóstico", "Diagnóstico de disco duro dañado", "Pruebas SMART y sectorización básica.", "fijo", 400, None, None, 0, "sucursal", "Mismo día"),

    # Mantenimiento preventivo y correctivo
    ("Mantenimiento preventivo y correctivo", "Limpieza interna de PC", "Limpieza de polvo y revisión general de componentes.", "fijo", 450, None, None, 0, "sucursal", "Mismo día"),
    ("Mantenimiento preventivo y correctivo", "Limpieza profunda de laptop", "Desarme y limpieza avanzada de portátil.", "fijo", 650, None, None, 0, "sucursal", "Mismo día"),
    ("Mantenimiento preventivo y correctivo", "Cambio de pasta térmica", "Aplicación de pasta térmica estándar.", "fijo", 250, None, None, 0, "sucursal", "Mismo día"),
    ("Mantenimiento preventivo y correctivo", "Cambio de pasta térmica premium", "Aplicación de pasta térmica de alto rendimiento.", "fijo", 400, None, None, 0, "sucursal", "Mismo día"),
    ("Mantenimiento preventivo y correctivo", "Mantenimiento preventivo completo", "Limpieza, optimización y revisión integral.", "fijo", 700, None, None, 0, "sucursal", "Mismo día"),
    ("Mantenimiento preventivo y correctivo", "Mantenimiento correctivo", "Corrección de problemas detectados en diagnóstico.", "desde", 900, None, None, 1, "sucursal", "1 a 3 días"),
    ("Mantenimiento preventivo y correctivo", "Limpieza de ventiladores", "Limpieza y balanceo de ventiladores.", "fijo", 300, None, None, 0, "sucursal", "Mismo día"),
    ("Mantenimiento preventivo y correctivo", "Optimización de temperatura", "Ajuste térmico para operación estable.", "fijo", 450, None, None, 0, "mixto", "Mismo día"),
    ("Mantenimiento preventivo y correctivo", "Revisión de sistema de enfriamiento", "Diagnóstico de flujo de aire y disipación.", "fijo", 350, None, None, 0, "sucursal", "Mismo día"),
    ("Mantenimiento preventivo y correctivo", "Cambio de ventiladores dañados", "Sustitución de ventiladores defectuosos.", "desde", 500, None, None, 1, "sucursal", "Mismo día"),

    # Software y sistema operativo
    ("Software y sistema operativo", "Instalación de Windows", "Instalación limpia y configuración inicial.", "fijo", 500, None, None, 0, "sucursal", "Mismo día"),
    ("Software y sistema operativo", "Licencia original de Windows", "Suministro e instalación de licencia oficial.", "desde", 2500, None, None, 0, "sucursal", "Mismo día"),
    ("Software y sistema operativo", "Activación de Windows", "Activación y validación del sistema.", "fijo", 300, None, None, 0, "remoto", "Mismo día"),
    ("Software y sistema operativo", "Instalación de Office", "Instalación y configuración de paquetería Office.", "fijo", 400, None, None, 0, "mixto", "Mismo día"),
    ("Software y sistema operativo", "Licencia original de Office", "Suministro de licencia oficial de Office.", "desde", 1800, None, None, 0, "mixto", "Mismo día"),
    ("Software y sistema operativo", "Instalación de programas esenciales", "Instalación de software básico de trabajo.", "fijo", 300, None, None, 0, "mixto", "Mismo día"),
    ("Software y sistema operativo", "Configuración inicial de equipo nuevo", "Puesta a punto y ajustes de primer uso.", "fijo", 450, None, None, 0, "mixto", "Mismo día"),
    ("Software y sistema operativo", "Instalación de drivers", "Instalación de controladores oficiales.", "fijo", 250, None, None, 0, "mixto", "Mismo día"),
    ("Software y sistema operativo", "Actualización de drivers", "Actualización segura de controladores.", "fijo", 300, None, None, 0, "mixto", "Mismo día"),
    ("Software y sistema operativo", "Formateo completo", "Respaldo básico e instalación limpia.", "fijo", 600, None, None, 0, "sucursal", "Mismo día"),
    ("Software y sistema operativo", "Particionado de discos", "Creación y ajuste de particiones.", "fijo", 300, None, None, 0, "sucursal", "Mismo día"),
    ("Software y sistema operativo", "Instalación Dual Boot", "Configuración de dos sistemas operativos.", "fijo", 700, None, None, 0, "sucursal", "1 día"),
    ("Software y sistema operativo", "Configuración de BIOS", "Ajustes de firmware y arranque.", "fijo", 350, None, None, 0, "sucursal", "Mismo día"),

    # Seguridad y optimización
    ("Seguridad y optimización", "Eliminación de virus", "Limpieza de amenazas comunes.", "fijo", 500, None, None, 0, "mixto", "Mismo día"),
    ("Seguridad y optimización", "Eliminación de malware", "Desinfección profunda de software malicioso.", "fijo", 550, None, None, 0, "mixto", "Mismo día"),
    ("Seguridad y optimización", "Eliminación de spyware", "Eliminación de software espía.", "fijo", 500, None, None, 0, "mixto", "Mismo día"),
    ("Seguridad y optimización", "Protección antivirus", "Instalación y configuración de suite de seguridad.", "fijo", 350, None, None, 0, "mixto", "Mismo día"),
    ("Seguridad y optimización", "Optimización del sistema", "Ajustes para mejorar desempeño general.", "fijo", 450, None, None, 0, "mixto", "Mismo día"),
    ("Seguridad y optimización", "Aceleración de arranque", "Optimización de inicio de sistema.", "fijo", 400, None, None, 0, "mixto", "Mismo día"),
    ("Seguridad y optimización", "Optimización para gaming", "Ajustes para rendimiento en juegos.", "fijo", 600, None, None, 0, "sucursal", "Mismo día"),
    ("Seguridad y optimización", "Limpieza de archivos basura", "Limpieza de temporales y optimización ligera.", "fijo", 250, None, None, 0, "mixto", "Mismo día"),
    ("Seguridad y optimización", "Configuración de seguridad de Windows", "Ajustes de seguridad y políticas básicas.", "fijo", 350, None, None, 0, "mixto", "Mismo día"),

    # Respaldo y recuperación
    ("Respaldo y recuperación", "Respaldo de información", "Respaldo de documentos y archivos del usuario.", "desde", 400, None, None, 0, "mixto", "Mismo día"),
    ("Respaldo y recuperación", "Migración de archivos", "Traslado de archivos a nuevo equipo/unidad.", "desde", 500, None, None, 0, "mixto", "Mismo día"),
    ("Respaldo y recuperación", "Recuperación de archivos eliminados", "Intento de recuperación en medios dañados/lógicos.", "desde", 800, None, None, 1, "sucursal", "1 a 3 días"),
    ("Respaldo y recuperación", "Recuperación de contraseñas", "Recuperación según escenario permitido.", "desde", 500, None, None, 1, "sucursal", "1 día"),
    ("Respaldo y recuperación", "Configuración de copias de seguridad automáticas", "Automatización de respaldos periódicos.", "fijo", 450, None, None, 0, "mixto", "Mismo día"),
    ("Respaldo y recuperación", "Transferencia de información entre equipos", "Traspaso completo entre computadoras.", "fijo", 500, None, None, 0, "mixto", "Mismo día"),
    ("Respaldo y recuperación", "Clonación de discos", "Clonado sector a sector o lógico.", "fijo", 700, None, None, 0, "sucursal", "Mismo día"),
    ("Respaldo y recuperación", "Migración de HDD a SSD", "Clonado y ajuste de arranque.", "fijo", 800, None, None, 0, "sucursal", "Mismo día"),

    # Upgrade y ensamblaje
    ("Upgrade y ensamblaje", "Actualización de memoria RAM", "Instalación y prueba de memoria RAM.", "fijo", 300, None, None, 0, "sucursal", "Mismo día"),
    ("Upgrade y ensamblaje", "Instalación de SSD", "Instalación física y ajuste de sistema.", "fijo", 350, None, None, 0, "sucursal", "Mismo día"),
    ("Upgrade y ensamblaje", "Cambio de procesador", "Sustitución de CPU y pruebas térmicas.", "fijo", 500, None, None, 0, "sucursal", "Mismo día"),
    ("Upgrade y ensamblaje", "Instalación de tarjeta gráfica", "Montaje y configuración de GPU.", "fijo", 450, None, None, 0, "sucursal", "Mismo día"),
    ("Upgrade y ensamblaje", "Cambio de fuente de poder", "Sustitución de PSU y validación eléctrica.", "fijo", 450, None, None, 0, "sucursal", "Mismo día"),
    ("Upgrade y ensamblaje", "Upgrade completo de PC", "Actualización integral de componentes.", "desde", 1200, None, None, 1, "sucursal", "1 a 2 días"),
    ("Upgrade y ensamblaje", "Ensamble de computadora personalizada", "Armado completo bajo requerimientos.", "desde", 1500, None, None, 1, "sucursal", "1 a 2 días"),
    ("Upgrade y ensamblaje", "Armado de PC Gamer", "Ensamble especializado para gaming.", "desde", 1800, None, None, 1, "sucursal", "1 a 2 días"),
    ("Upgrade y ensamblaje", "Armado de PC para oficina", "Ensamble optimizado para productividad.", "desde", 1200, None, None, 1, "sucursal", "1 a 2 días"),
    ("Upgrade y ensamblaje", "Configuración de RGB y rendimiento", "Ajuste visual y de perfiles de potencia.", "fijo", 400, None, None, 0, "sucursal", "Mismo día"),

    # Redes y conectividad
    ("Redes y conectividad", "Configuración de red local", "Configuración de red doméstica/oficina pequeña.", "fijo", 500, None, None, 0, "domicilio", "Mismo día"),
    ("Redes y conectividad", "Instalación de impresoras", "Instalación y configuración en red o local.", "fijo", 350, None, None, 0, "mixto", "Mismo día"),
    ("Redes y conectividad", "Configuración de WiFi", "Ajustes de cobertura y seguridad WiFi.", "fijo", 300, None, None, 0, "domicilio", "Mismo día"),
    ("Redes y conectividad", "Solución de problemas de internet", "Diagnóstico de conectividad y estabilidad.", "fijo", 450, None, None, 0, "domicilio", "Mismo día"),
    ("Redes y conectividad", "Configuración de router", "Ajustes avanzados de router.", "fijo", 400, None, None, 0, "domicilio", "Mismo día"),
    ("Redes y conectividad", "Compartición de archivos en red", "Configuración de carpetas y permisos en red.", "fijo", 500, None, None, 0, "domicilio", "Mismo día"),
    ("Redes y conectividad", "Configuración de acceso remoto", "Habilitación segura de acceso remoto.", "fijo", 600, None, None, 0, "mixto", "Mismo día"),

    # Servicios premium
    ("Servicios premium", "Instalación de juegos", "Instalación y configuración básica de juegos.", "fijo", 250, None, None, 0, "mixto", "Mismo día"),
    ("Servicios premium", "Optimización para streaming", "Ajustes para plataformas de transmisión.", "fijo", 700, None, None, 0, "sucursal", "Mismo día"),
    ("Servicios premium", "Configuración para edición de video", "Optimización de software y recursos para edición.", "fijo", 800, None, None, 0, "sucursal", "Mismo día"),
    ("Servicios premium", "Configuración para diseño gráfico", "Ajustes para flujo de trabajo de diseño.", "fijo", 700, None, None, 0, "sucursal", "Mismo día"),
    ("Servicios premium", "Setup para Home Office", "Configuración integral para trabajo remoto.", "fijo", 600, None, None, 0, "domicilio", "Mismo día"),
    ("Servicios premium", "Setup para oficina empresarial", "Preparación de estaciones en oficina.", "desde", 1200, None, None, 1, "domicilio", "1 a 2 días"),
    ("Servicios premium", "Soporte técnico remoto", "Asistencia remota por sesión.", "desde", 300, None, None, 0, "remoto", "Mismo día"),
    ("Servicios premium", "Servicio a domicilio", "Atención en ubicación del cliente.", "rango", 0, 150, 500, 0, "domicilio", "Mismo día"),
    ("Servicios premium", "Soporte urgente express", "Atención prioritaria con recargo.", "recargo", 500, None, None, 0, "mixto", "Inmediato"),

    # Servicios empresariales
    ("Servicios empresariales", "Mantenimiento a empresas", "Servicio integral para equipos empresariales.", "desde", 2500, None, None, 1, "domicilio", "Según contrato"),
    ("Servicios empresariales", "Soporte a oficinas", "Soporte técnico continuo para oficinas.", "desde", 2000, None, None, 1, "domicilio", "Según contrato"),
    ("Servicios empresariales", "Control e inventario de hardware", "Levantamiento y control de activos TI.", "desde", 1500, None, None, 1, "domicilio", "1 a 3 días"),
    ("Servicios empresariales", "Instalación masiva de software", "Despliegue de software en múltiples equipos.", "desde", 2000, None, None, 1, "domicilio", "1 a 3 días"),
    ("Servicios empresariales", "Redes internas empresariales", "Implementación y ajuste de red interna.", "desde", 3000, None, None, 1, "domicilio", "1 a 5 días"),
    ("Servicios empresariales", "Respaldos corporativos", "Estrategia y ejecución de respaldos empresariales.", "desde", 2500, None, None, 1, "domicilio", "1 a 3 días"),
    ("Servicios empresariales", "Soporte mensual por contrato", "Servicio recurrente mensual empresarial.", "desde", 5000, None, None, 1, "domicilio", "Mensual"),
]


def main():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("DELETE FROM servicios")
        cursor.execute("ALTER TABLE servicios AUTO_INCREMENT = 1")

        cursor.executemany(
            """
            INSERT INTO servicios (
                categoria, nombre, descripcion, tipo_precio, precio, precio_min, precio_max,
                requiere_diagnostico, modalidad, tiempo_estimado, activo
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
            """,
            SERVICIOS,
        )

        conexion.commit()
        print(f"Catálogo de servicios cargado correctamente: {len(SERVICIOS)} registros.")
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":
    main()
