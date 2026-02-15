#!/usr/bin/env python3
"""
GENERADOR DE CAPA 3: PROBLEMATIZACIÓN CONTEMPORÁNEA
====================================================

Genera las 19 problematizaciones (1000-1500 palabras) que conectan
los conceptos genealógicos de CAPA 2 con presente algorítmico.

Dependencias:
- CAPA0: TSR101-120QUOTES.md (fragmentos fundacionales)
- CAPA1: Bibliografía verificada
- CAPA2: Genealogías conceptuales
- GLOSARIO_CICLOPE.json

Uso:
    python generar_capa3.py --modelo claude --tsr 102
    python generar_capa3.py --modelo sonar --all
    python generar_capa3.py --validar-antes
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

GLOSARIO_PATH = Path("config/GLOSARIO_CICLOPE.json")
METADATOS_PATH = Path("config/METADATOS_PROYECTO.json")
CAPAS_DIR = Path("capas")

CAPA0_PATH = CAPAS_DIR / "CAPA0_semilla" / "TSR101-120QUOTES.md"
CAPA1_PATH = CAPAS_DIR / "CAPA1_bibliografia" / "TSR_CAPA1_FINAL.json"
CAPA2_PATH = CAPAS_DIR / "CAPA2_genealogia" / "TSR_CAPA2_FINAL.json"

OUTPUT_PATH = CAPAS_DIR / "CAPA3_problematizacion" / "TSR_CAPA3_FINAL.json"

# ============================================================================
# PROMPT TEMPLATE PARA CAPA 3
# ============================================================================

PROMPT_CAPA3_TEMPLATE = """
# TAREA: Genera la PROBLEMATIZACIÓN CONTEMPORÁNEA de TSR{tsr_id}

## CONTEXTO PREVIO (CAPAS ANTERIORES)

### CAPA 0: Fragmento fundacional
{fragmento_inicial}

### CAPA 2: Genealogía del concepto
{genealogia_resumen}

## TU TAREA AHORA (CAPA 3)

Escribe la **problematización contemporánea** del concepto, conectándolo con:
- Inteligencia Artificial (LLMs, autoría algorítmica, generación automática)
- NFT y blockchain (arte digital, tokenización, escasez programada)
- Plataformas digitales (redes sociales, algoritmos, economía atención)
- Cultura visual algorítmica (deepfakes, filtros, realidad aumentada)

## ESTRUCTURA REQUERIDA (1000-1500 palabras)

### 1. APERTURA TRANSICIONAL (100-150 palabras)
- Retoma el concepto de CAPA 2
- Plantea la tensión con el presente algorítmico
- Formula pregunta inicial que no se responderá del todo

**Ejemplo para TSR102 (Aura):**
"La reproductibilidad técnica que Benjamin diagnosticó en 1936 se ha radicalizado: 
ya no reproducimos copias físicas, sino que generamos infinitas variaciones sintéticas. 
¿Qué es el aura cuando la 'manifestación irrepetible de una lejanía' puede ser 
programada mediante algoritmos? Los NFT prometen resucitar el aura mediante 
escasez criptográfica, pero ¿no es precisamente esa escasez una simulación del 
aura que Benjamin declaró muerta?"

### 2. PROBLEMATIZACIÓN EN PRESENTE (600-900 palabras)

Desarrolla 3-4 problematizaciones específicas. Por ejemplo:

**A) IA y autoría algorítmica**
- ChatGPT, Claude, Midjourney: ¿quién es autor?
- Función-autor (Foucault) en era de coautoría máquina-humano
- Contratos que especifican "texto humano sin IA": ¿qué defienden?

**B) NFT y economía del arte digital**
- Escasez programada vs. reproductibilidad infinita
- Aura como metadata (certificado blockchain)
- Beeple, Grimes, artistas cripto: ¿resucitan aura o la parodian?

**C) Plataformas y economía atencional**
- TikTok, Instagram: fragmentación vs. totalidad
- Algoritmos de recomendación como nuevos "archivos" foucaultianos
- ¿Qué cuenta como conocimiento válido en feeds personalizados?

**D) Deepfakes y verdad sintética**
- Indistinguibilidad entre real y generado
- Epistemes algorítmicas: ¿qué regímenes de verdad producen?
- Post-verdad como condición epistémica, no solo política

### 3. RESONANCIA CON REFLEJOS HÍBRIDOS (100-150 palabras)
- Conecta con el universo narrativo/visual RH
- Identidades fragmentadas, archivos generativos
- Cíclope como método de visión situada

### 4. CIERRE ABIERTO (100-150 palabras)
- NO cierres con respuestas definitivas
- Plantea preguntas adicionales
- Abre hacia aplicación pedagógica (CAPA 6)

**Ejemplo de cierre abierto:**
"Si la educación reproduce estructuras de poder mediante certificaciones 
que validan quién puede hablar, ¿cómo cambian esas estructuras cuando 
los estudiantes co-escriben con IA? ¿Qué significa 'voz propia' en un 
ecosistema donde la escritura es negociación con sistemas probabilísticos? 
Las instituciones educativas responden prohibiendo IA o exigiendo 
declaraciones de 'trabajo humano'. Pero esa respuesta revela que no saben 
cómo leer textos híbridos. Y ahí es donde la lectura de segundo orden 
se vuelve urgente."

## INSTRUCCIONES CRÍTICAS

### TONO Y MÉTODO
- ✅ Español mexicano (no rioplatense, no neutro académico)
- ✅ Método socrático: preguntas que arden, no respuestas que cierran
- ✅ Crítico sin ser nihilista: exponer problemas sin proponer soluciones fáciles
- ✅ Interpela al lector: "¿Te has preguntado...?", "Observa lo que pasa cuando..."
- ❌ NO usar bullet points ni numeración visible
- ❌ NO cerrar con conclusiones definitivas
- ❌ NO mencionar "en conclusión", "para finalizar", etc.

### VALIDACIÓN TERMINOLÓGICA
Estos términos deben usarse según el GLOSARIO_CICLOPE.json:
{terminos_clave}

Si usas un término con múltiples definiciones (ej: "fragmento"), 
DEBES especificar cuál definición activas:
- ✅ "El fragmento (según Schlegel, con promesa de totalidad)..."
- ✅ "El fragmento blanchotiano (sin síntesis posible)..."
- ❌ "El fragmento..." (sin especificar cuál definición)

### CITAS Y REFERENCIAS
- Usa citas de CAPA 1 cuando sea relevante
- Formato: [Autor, año] inline
- NO inventes citas ni autores
- Puedes mencionar eventos actuales 2024-2026

## EXTENSIÓN
- Mínimo: 1000 palabras
- Máximo: 1500 palabras
- Ideal: 1200 palabras

## AHORA GENERA LA PROBLEMATIZACIÓN PARA TSR{tsr_id}
"""

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def cargar_json(path: Path) -> Dict:
    """Carga archivo JSON"""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def cargar_fragmento_inicial(tsr_id: int) -> str:
    """Extrae el fragmento fundacional de CAPA 0"""
    # TODO: Implementar parser de TSR101-120QUOTES.md
    # Por ahora retorna placeholder
    return f"[Fragmento fundacional de TSR{tsr_id}]"

def cargar_genealogia(tsr_id: int, capa2_data: Dict) -> str:
    """Extrae resumen de la genealogía de CAPA 2"""
    for tsr in capa2_data.get('estructura', []):
        if tsr.get('tsr') == tsr_id:
            genealogia = tsr.get('genealogia', '')
            # Extraer primeros 300 caracteres como resumen
            return genealogia[:300] + "..." if len(genealogia) > 300 else genealogia
    return "[Genealogía no encontrada]"

def generar_prompt_capa3(tsr_id: int, glosario: Dict, capa2: Dict) -> str:
    """Genera el prompt completo para un TSR específico"""
    
    fragmento = cargar_fragmento_inicial(tsr_id)
    genealogia = cargar_genealogia(tsr_id, capa2)
    
    # Extraer términos clave relevantes para este TSR
    terminos_clave = glosario['validacion_coherencia']['terminos_clave_rastreados']
    terminos_str = "\n".join([f"- {t}" for t in terminos_clave])
    
    return PROMPT_CAPA3_TEMPLATE.format(
        tsr_id=tsr_id,
        fragmento_inicial=fragmento,
        genealogia_resumen=genealogia,
        terminos_clave=terminos_str
    )

def validar_extensio(texto: str) -> tuple[bool, int]:
    """Valida que la extensión esté en rango 1000-1500 palabras"""
    palabras = len(texto.split())
    valido = 1000 <= palabras <= 1500
    return valido, palabras

def guardar_resultado(resultados: Dict, output_path: Path):
    """Guarda los resultados en JSON"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados en: {output_path}")

# ============================================================================
# GENERADOR PRINCIPAL
# ============================================================================

def generar_capa3_tsr(
    tsr_id: int,
    modelo: str,
    glosario: Dict,
    capa2: Dict
) -> Dict:
    """
    Genera la problematización de un TSR específico.
    
    Args:
        tsr_id: Número del TSR (102-120)
        modelo: 'claude' o 'sonar'
        glosario: Diccionario del glosario cargado
        capa2: Datos de CAPA 2
    
    Returns:
        Dict con la problematización generada
    """
    print(f"\n📝 Generando CAPA 3 para TSR{tsr_id}...")
    
    # Generar prompt
    prompt = generar_prompt_capa3(tsr_id, glosario, capa2)
    
    # TODO: Integrar con API de Claude o Sonar
    # Por ahora, placeholder
    problematizacion = f"[Problematización de TSR{tsr_id} generada con {modelo}]"
    
    # Validar extensión
    valida, num_palabras = validar_extensio(problematizacion)
    
    if not valida:
        print(f"⚠️  ADVERTENCIA: TSR{tsr_id} tiene {num_palabras} palabras (esperado: 1000-1500)")
    
    return {
        "tsr": tsr_id,
        "problematizacion": problematizacion,
        "num_palabras": num_palabras,
        "validacion_extension": valida,
        "modelo_usado": modelo,
        "fecha_generacion": datetime.now().isoformat()
    }

# ============================================================================
# CLI
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Genera CAPA 3 (Problematización contemporánea) del proyecto Cíclope TSR'
    )
    parser.add_argument('--modelo', choices=['claude', 'sonar'], default='claude',
                       help='Modelo de LLM a usar')
    parser.add_argument('--tsr', type=int, help='TSR específico a generar (102-120)')
    parser.add_argument('--all', action='store_true', help='Generar todos los TSR')
    parser.add_argument('--validar-antes', action='store_true',
                       help='Validar coherencia de CAPA 2 antes de generar')
    parser.add_argument('--output', help='Ruta de salida personalizada')
    
    args = parser.parse_args()
    
    # Cargar dependencias
    print("📖 Cargando dependencias...")
    glosario = cargar_json(GLOSARIO_PATH)
    metadatos = cargar_json(METADATOS_PATH)
    capa2 = cargar_json(CAPA2_PATH)
    
    print("✅ Dependencias cargadas\n")
    
    # Validar CAPA 2 si se solicita
    if args.validar_antes:
        print("🔍 Validando coherencia de CAPA 2...")
        os.system("python validar_coherencia_capas.py --capa CAPA2 --all")
        print()
    
    # Determinar rango de TSR a generar
    if args.all:
        tsr_range = range(102, 121)
    elif args.tsr:
        tsr_range = [args.tsr]
    else:
        print("❌ ERROR: Especifica --tsr N o --all")
        return
    
    # Generar problematizaciones
    resultados = {
        "metadata": {
            "capa": "CAPA 3: Problematización contemporánea",
            "fecha_generacion": datetime.now().isoformat(),
            "total_tsr": len(tsr_range),
            "modelo": args.modelo
        },
        "estructura": []
    }
    
    for tsr_id in tsr_range:
        resultado_tsr = generar_capa3_tsr(tsr_id, args.modelo, glosario, capa2)
        resultados["estructura"].append(resultado_tsr)
    
    # Guardar resultados
    output_path = Path(args.output) if args.output else OUTPUT_PATH
    guardar_resultado(resultados, output_path)
    
    # Estadísticas finales
    total_palabras = sum(r['num_palabras'] for r in resultados['estructura'])
    promedio = total_palabras / len(resultados['estructura'])
    
    print(f"\n{'='*60}")
    print(f"ESTADÍSTICAS FINALES")
    print(f"{'='*60}")
    print(f"TSR generados: {len(resultados['estructura'])}")
    print(f"Palabras totales: {total_palabras:,}")
    print(f"Promedio por TSR: {promedio:.0f} palabras")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
