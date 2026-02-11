"""
TSR Generator with Web Search

Este script genera un TSR (The Second Order Read) siguiendo la plantilla PLANTILLATSR.md
utilizando la API de Perplexity con búsqueda web habilitada.

Variables requeridas en .env:
- PERPLEXITY_API_KEY: Tu clave de API de Perplexity
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, List, Optional

# Cargar variables de entorno
load_dotenv()

# Configuración de la API
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
API_URL = "https://api.perplexity.ai/chat/completions"

# Encabezados para la petición
HEADERS = {
    "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
    "Content-Type": "application/json"
}

# Variables del TSR (ejemplo para TSR102 - Walter Benjamin)
TSR_VARS = {
    "TSR_NUMBER": "102",
    "TITLE": "Aura Resucitada",
    "AUTHOR": "Walter Benjamin",
    "WORK": "La obra de arte en la época de su reproductibilidad técnica",
    "YEAR": "1936",
    "OPENING_QUOTE": "La técnica desvincula lo reproducido del ámbito de la tradición. Multiplica las reproducciones, poniendo una presencia masiva en lugar de una presencia irrepetible. El aura muere cuando todo se copia.",
    "KEYWORDS": "aura, reproductibilidad técnica, Benjamin, arte contemporáneo, digital",
    "RH_NUMBER": "102",
    "PUBLICATION_DATE": datetime.now().strftime("%d.%m.%Y"),
    "PRICE": "15",
    "AUTHOR_EMAIL": "sarayu@trace.edu.mx"
}

def generate_tsr_prompt(tsr_vars: Dict) -> str:
    """Genera el prompt para la API de Perplexity siguiendo PLANTILLATSR.md"""
    return f"""
    Eres un experto en análisis crítico siguiendo la metodología TRCO. 
    Generarás un TSR (The Second Order Read) con la siguiente estructura exacta:
    
    # CLÚSTER I • TSR{tsr_vars["TSR_NUMBER"]} | {tsr_vars["TITLE"]}
    
    # {tsr_vars["AUTHOR"]} — {tsr_vars["WORK"]} ({tsr_vars["YEAR"]})
    
    > {tsr_vars["OPENING_QUOTE"]}
    
    Interrogante abierto: [Formular una pregunta clave que atraviese el análisis]
    
    ---
    
    [Continuar con la estructura completa de 24 secciones según PLANTILLATSR.md]
    
    INSTRUCCIONES CRÍTICAS:
    - Usar search_web para verificar TODAS las citas y referencias
    - No inventar KPIs, métricas ni porcentajes
    - Mantener tono institucional TRACE, sin lenguaje de marketing
    - Precio fijo: ${tsr_vars["PRICE"]} USD
    - Extensión mínima: 3,300 palabras de contenido crítico
    - Seguir estructura exacta de 24 secciones
    - Conectar con TSR anterior (genealogía) y siguiente (siembra)
    - Usar sistema TRCO (no TRACE v4/v5)
    - Incluir 12-14 fuentes verificables
    - Incluir Caso de Estudio + Teaser Substack + Guión Taller
    
    PROHIBIDO:
    - KPIs, métricas, porcentajes inventados
    - Versiones "TRACE v4/v5" (solo existe TRCO)
    - Checkpoints de aprobación ([✓] Validado)
    - Precio diferente a $15 USD
    - Tono marketero
    - Código ejecutable decorativo
    - Licencias inventadas
    - Emojis checkmarks, bullets decorativos
    - Acortar secciones
    """

def call_perplexity_api(prompt: str, search_web: bool = True) -> str:
    """Llama a la API de Perplexity con el prompt dado"""
    payload = {
        "model": "sonar-medium-online",
        "messages": [{"role": "user", "content": prompt}],
        "search_web": search_web,
        "max_tokens": 8000,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error al llamar a la API de Perplexity: {e}")
        return ""

def save_tsr_to_file(content: str, tsr_vars: Dict):
    """Guarda el TSR generado en un archivo"""
    filename = f"TSR{tsr_vars['TSR_NUMBER']}_{tsr_vars['TITLE'].replace(' ', '_')}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"TSR guardado en: {filename}")

def main():
    # Verificar clave de API
    if not PERPLEXITY_API_KEY:
        print("Error: No se encontró PERPLEXITY_API_KEY en las variables de entorno")
        print("Por favor crea un archivo .env con tu clave de API")
        return
    
    print(f"Generando TSR{TSR_VARS['TSR_NUMBER']} - {TSR_VARS['TITLE']}...")
    
    # Generar el prompt
    prompt = generate_tsr_prompt(TSR_VARS)
    
    # Llamar a la API de Perplexity
    print("Llamando a la API de Perplexity (esto puede tardar unos minutos)...")
    tsr_content = call_perplexity_api(prompt, search_web=True)
    
    if tsr_content:
        # Guardar el TSR generado
        save_tsr_to_file(tsr_content, TSR_VARS)
        print("¡TSR generado exitosamente!")
    else:
        print("No se pudo generar el TSR. Por favor revisa los errores.")

if __name__ == "__main__":
    main()
