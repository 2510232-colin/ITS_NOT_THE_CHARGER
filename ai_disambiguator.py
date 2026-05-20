import json
import os
import re
from typing import Any

import google.generativeai as genai


def _construir_prompt(consulta: str, candidatos: list[dict[str, Any]]) -> str:
    candidatos_json = json.dumps(candidatos, ensure_ascii=False)
    return (
        "Eres un clasificador de intención para un sistema de soporte técnico en México.\n"
        "Tu tarea es elegir el servicio MÁS probable según la consulta del usuario.\n\n"
        "Reglas:\n"
        "- Debes elegir SOLO un servicio de la lista.\n"
        "- NO inventes servicios.\n"
        "- id_servicio debe ser uno de los IDs de candidatos o null.\n"
        "- Si ningún candidato coincide claramente, responde id_servicio=null.\n"
        "- Prioriza intención principal del usuario, no palabras aisladas.\n"
        "- Si hay duda entre dos opciones, elige la más específica para el problema descrito.\n"
        "- Responde SOLO JSON válido.\n\n"
        "Formato exacto:\n"
        '{"id_servicio": <int|null>, "motivo": "<breve>"}\n\n'
        f"Consulta del usuario:\n{consulta}\n\n"
        f"Candidatos:\n{candidatos_json}\n"
    )


def _extraer_json(texto: str) -> dict[str, Any] | None:
    texto = (texto or "").strip()
    if not texto:
        return None

    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", texto, flags=re.DOTALL)
    if not match:
        return None

    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


def desempatar_servicio_con_gemini(consulta: str, candidatos: list[dict[str, Any]]) -> int | None:
    api_key = (os.getenv("GEMINI_API_KEY") or "").strip()
    if not api_key or not candidatos:
        return None

    modelo = "gemini-1.5-flash"

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(modelo)
        prompt = _construir_prompt(consulta, candidatos)
        response = model.generate_content(prompt)
        payload = _extraer_json(getattr(response, "text", ""))
        if not payload:
            return None

        servicio_id = payload.get("id_servicio")
        if servicio_id is None:
            return None

        try:
            servicio_id = int(servicio_id)
        except (TypeError, ValueError):
            return None

        ids_validos = {int(item.get("id")) for item in candidatos if item.get("id") is not None}
        return servicio_id if servicio_id in ids_validos else None
    except Exception:
        return None
