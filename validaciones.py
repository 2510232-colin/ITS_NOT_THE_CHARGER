import re
import unicodedata


PATRON_CORREO = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PATRON_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s]{2,60}$")
PATRON_TELEFONO = re.compile(r"^\d{10}$")
PATRON_CONTRASENA = re.compile(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^\w\s]).{8,}$")
PATRON_CARACTERES_PELIGROSOS = re.compile(r"(--|;|/\*|\*/|\bunion\b|\bselect\b|\bdrop\b|\binsert\b)", re.IGNORECASE)


def limpiar_texto(valor):
    return (valor or "").strip()


def limpiar_espacios(valor):
    texto = limpiar_texto(valor)
    return re.sub(r"\s+", " ", texto)


def quitar_acentos(texto):
    base = unicodedata.normalize("NFD", texto or "")
    return "".join(char for char in base if unicodedata.category(char) != "Mn")


def normalizar_texto(valor, minusculas=False, sin_acentos=False):
    texto = limpiar_espacios(valor)
    if minusculas:
        texto = texto.lower()
    if sin_acentos:
        texto = quitar_acentos(texto)
    return texto


def normalizar_lista_csv(valor):
    texto = limpiar_espacios(valor)
    if not texto:
        return ""

    partes = re.split(r"[,;\n]+", texto)
    resultado = []
    vistos = set()

    for parte in partes:
        item = limpiar_espacios(parte)
        if not item:
            continue
        llave = normalizar_texto(item, minusculas=True, sin_acentos=True)
        if llave in vistos:
            continue
        vistos.add(llave)
        resultado.append(item)

    return ", ".join(resultado)


def normalizar_prioridad(valor, predeterminado=3, minimo=1, maximo=5):
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        numero = predeterminado
    return max(minimo, min(maximo, numero))


def validar_correo(correo):
    correo_limpio = limpiar_texto(correo).lower()
    if not PATRON_CORREO.match(correo_limpio):
        return False, "El correo no tiene un formato válido."
    return True, ""


def validar_nombre(nombre, etiqueta="nombre"):
    nombre_limpio = limpiar_texto(nombre)
    if not PATRON_NOMBRE.match(nombre_limpio):
        return False, f"El campo {etiqueta} solo permite letras y espacios (2 a 60 caracteres)."
    return True, ""


def validar_telefono(numero):
    telefono_limpio = limpiar_texto(numero)
    if not PATRON_TELEFONO.match(telefono_limpio):
        return False, "El número telefónico debe tener 10 dígitos."
    return True, ""


def validar_contrasena(contrasena):
    if not PATRON_CONTRASENA.match(contrasena or ""):
        return False, "La contraseña debe tener mínimo 8 caracteres, mayúscula, minúscula, número y carácter especial."
    return True, ""


def validar_texto_seguro(valor, etiqueta="campo", minimo=2, maximo=200):
    texto = limpiar_texto(valor)
    if len(texto) < minimo or len(texto) > maximo:
        return False, f"El campo {etiqueta} debe tener entre {minimo} y {maximo} caracteres."
    if PATRON_CARACTERES_PELIGROSOS.search(texto):
        return False, f"El campo {etiqueta} contiene caracteres o patrones no permitidos."
    return True, ""


def validar_lista_csv(valor, etiqueta="lista", maximo=1200):
    texto = normalizar_lista_csv(valor)
    if not texto:
        return True, "", ""
    if len(texto) > maximo:
        return False, f"El campo {etiqueta} excede el tamaño permitido.", ""
    if PATRON_CARACTERES_PELIGROSOS.search(texto):
        return False, f"El campo {etiqueta} contiene patrones no permitidos.", ""
    return True, "", texto


def validar_prioridad_rango(valor, minimo=1, maximo=5):
    numero = normalizar_prioridad(valor, predeterminado=3, minimo=minimo, maximo=maximo)
    return True, "", numero
