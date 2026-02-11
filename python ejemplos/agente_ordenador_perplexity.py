# AGENTE_ORDENADOR v2.0 - Prompt con Playbook Integrado para Perplexity Research API

import requests
import json
import os

# Prompt para generar TSR102 con estructura TSR101 y contenido de @[TSR101-120QUOTES.md]
TSR_GENERATION_PROMPT = """
Genera TSR102 "Aura Resucitada" basado en el fragmento de Walter Benjamin sobre aura de @[TSR101-120QUOTES.md]:

"## TSR120 Leer para dejar de ser el mismo.
Chartier recuerda que leer no es solo aprender, sino aprender a ver de otro modo el propio mundo. Freire agrega que la alfabetización auténtica convierte al sujeto en protagonista de su historia. Una lectura de segundo orden no busca "llevarse una idea clara", sino ponerse en riesgo. Si cierras un texto siendo exactamente la misma persona, no leíste: solo consumiste información."

Sigue exactamente la estructura y formato de @[CLÚSTER I • TSR101.md]: nota apertura, genealogía, problematización, resonancias con Reflejos Híbridos, glitch final.

Tema: "Asesinato del autor como acto de misericordia aplicado a aura".

KPIs del playbook: Iteración v2-v5 si necesaria, balance 50/50 técnico-narrativo, aprobación explícita, meta 116 fragmentos.

Output: Texto completo en .md, listo para PDF.
"""

# Código para llamar a Perplexity Research API
def call_perplexity_api(user_message, api_key=None):
    """
    Envía el prompt de AGENTE_ORDENADOR a Perplexity Research API.
    
    Args:
        user_message (str): Mensaje del usuario para AGENTE_ORDENADOR.
        api_key (str): API Key de Perplexity. Si None, usa variable de entorno.
    
    Returns:
        dict: Respuesta de la API.
    """
    if api_key is None:
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            raise ValueError("API Key de Perplexity no encontrada. Configura PERPLEXITY_API_KEY o pásala como argumento.")
    
    url = "https://api.perplexity.ai/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Sistema prompt es AGENTE_ORDENADOR_PROMPT
    # Usuario message es el input específico
    data = {
        "model": "sonar-pro",  # O "sonar" según disponibilidad
        "messages": [
            {"role": "system", "content": AGENTE_ORDENADOR_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 4000,  # Ajustar según límites
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error en API: {response.status_code} - {response.text}")

# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo: Generar prompt para TSR102
    user_input = "Genera el prompt completo para TRACE TSR102 'Aura Resucitada', basado en el fragmento de Benjamin sobre aura. Incluye validación contra TSR101 y KPIs del playbook."
    
    try:
        result = call_perplexity_api(user_input)
        print("Respuesta de AGENTE_ORDENADOR:")
        print(result["choices"][0]["message"]["content"])
    except Exception as e:
        print(f"Error: {e}")
