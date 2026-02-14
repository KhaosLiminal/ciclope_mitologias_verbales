"""
TSR_CAPA2_Resumenes.py
Genera resúmenes conceptuales de 150-200 palabras para cada TSR
RUTA CORREGIDA: cíclope_en_siete_capas/scripts/
"""

import json
import time
import os
from datetime import datetime
from openai import OpenAI

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# API de Perplexity
API_KEY = "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"
client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

# Rutas (relativas a la carpeta scripts donde está este archivo)
ARCHIVO_ENTRADA = "TSR_CAPA1_FINAL.json"
ARCHIVO_SALIDA = "TSR_CAPA2_Resumenes.json"

# Verificar que estamos en la carpeta correcta
if not os.path.exists(ARCHIVO_ENTRADA):
    print("❌ ERROR: No se encuentra TSR_CAPA1_FINAL.json")
    print(f"📂 Ubicación actual: {os.getcwd()}")
    print(f"💡 Asegúrate de ejecutar desde: cíclope_en_siete_capas/scripts/")
    exit(1)

# Parámetros
MODELO = "sonar-pro"
MAX_TOKENS = 2500
TEMPERATURA = 0.7
DELAY_SEGUNDOS = 6

# ============================================================================
# PROMPT PARA RESÚMENES
# ============================================================================

PROMPT_TEMPLATE = """Eres un teórico literario especializado en teoría crítica y filosofía contemporánea.

**CONTEXTO DEL PROYECTO:**
"Reflejos Híbridos" es un universo narrativo que explora identidades fragmentadas, archivos como estructuras generativas, y la tensión entre materialidad textual y desmaterialización digital.

**TSR (Tensor Semántico-Retórico) a resumir:**
- **Número:** {numero_tsr}
- **Título:** {titulo}
- **Cluster:** {cluster}

**FUENTES BIBLIOGRÁFICAS DISPONIBLES:**
{fuentes}

---

**TAREA:**
Redacta un resumen conceptual de **150-200 palabras exactas** con esta estructura:

**1. CONCEPTO CENTRAL (40-50 palabras)**
Define el concepto teórico principal y su contexto epistémico.

**2. APORTACIÓN DEL AUTOR PRIMARIO (40-50 palabras)**
Explica la tesis central y la innovación conceptual del autor principal citado en el TSR.

**3. DIÁLOGO CON AUTORES SECUNDARIOS (30-40 palabras)**
Establece convergencias y tensiones con otros teóricos de las fuentes bibliográficas.

**4. CONEXIÓN CON REFLEJOS HÍBRIDOS (30-40 palabras)**
Vincula el concepto con el universo narrativo: identidades fragmentadas, archivos como estructuras generativas, o materialidad/desmaterialización textual.

---

**REQUISITOS:**
- Vocabulario académico preciso
- Citas conceptuales (sin comillas, integradas al texto)
- Tono analítico y denso
- NO uses enumeración explícita (1, 2, 3, 4)
- Flujo continuo entre secciones
- Total: 150-200 palabras

**FORMATO DE SALIDA:**
Redacta un solo párrafo cohesionado que integre las cuatro secciones de manera orgánica.
"""

# ============================================================================
# FUNCIONES
# ============================================================================

def cargar_tsr_capa1():
    """Carga los TSRs de CAPA 1"""
    print(f"\n📂 Cargando: {ARCHIVO_ENTRADA}")
    
    with open(ARCHIVO_ENTRADA, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    # Extraer TSRs según estructura
    tsr_list = []
    
    if 'clusters' in datos:
        for cluster_nombre, tsrs in datos['clusters'].items():
            for tsr in tsrs:
                tsr['cluster'] = cluster_nombre
                tsr_list.append(tsr)
    elif 'resultados' in datos:
        tsr_list = datos['resultados']
    
    # Ordenar por número de TSR
    tsr_list.sort(key=lambda x: int(x.get('tsr', 0)))
    
    print(f"   ✅ {len(tsr_list)} TSRs cargados")
    return tsr_list, datos.get('metadata', {})


def formatear_fuentes(fuentes):
    """Formatea las fuentes bibliográficas para el prompt"""
    fuentes_texto = []
    
    for i, fuente in enumerate(fuentes, 1):
        autor = fuente.get('autor', 'Autor desconocido')
        titulo = fuente.get('titulo', 'Sin título')
        año = fuente.get('año', 'S/F')
        bloque = fuente.get('bloque', 'Sin clasificar')
        
        fuentes_texto.append(
            f"[{i}] {autor} ({año}): {titulo} [{bloque}]"
        )
    
    return "\n".join(fuentes_texto)


def generar_resumen(tsr):
    """Genera resumen conceptual para un TSR usando Perplexity"""
    numero_tsr = tsr.get('tsr', 'N/A')
    titulo = tsr.get('titulo', 'Sin título')
    cluster = tsr.get('cluster', 'Sin cluster')
    fuentes = tsr.get('fuentes', [])
    
    # Formatear fuentes
    fuentes_texto = formatear_fuentes(fuentes)
    
    # Construir prompt
    prompt = PROMPT_TEMPLATE.format(
        numero_tsr=numero_tsr,
        titulo=titulo,
        cluster=cluster,
        fuentes=fuentes_texto
    )
    
    # Llamada a API
    try:
        response = client.chat.completions.create(
            model=MODELO,
            messages=[
                {
                    "role": "system",
                    "content": "Eres un teórico literario especializado en teoría crítica contemporánea. Redactas resúmenes densos y precisos con vocabulario académico."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURA
        )
        
        resumen = response.choices[0].message.content.strip()
        
        # Contar palabras
        num_palabras = len(resumen.split())
        
        return {
            "resumen": resumen,
            "num_palabras": num_palabras,
            "exito": True
        }
    
    except Exception as e:
        return {
            "resumen": None,
            "error": str(e),
            "exito": False
        }


# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

def main():
    print("=" * 80)
    print("📝 CAPA 2: RESÚMENES CONCEPTUALES")
    print("=" * 80)
    print(f"📂 Carpeta de trabajo: {os.getcwd()}")
    
    # Cargar TSRs
    tsr_list, metadata_original = cargar_tsr_capa1()
    
    print(f"\n🎯 TSRs a procesar: {len(tsr_list)}")
    print(f"📊 Costo estimado: ${len(tsr_list) * 0.004:.2f} USD")
    print(f"⏱️  Tiempo estimado: ~{len(tsr_list) * 6 // 60 + 1} minutos")
    
    input("\n🚀 Presiona ENTER para comenzar...")
    
    # Procesar TSRs
    resultados = []
    exitosos = 0
    fallidos = 0
    
    print("\n" + "=" * 80)
    
    for i, tsr in enumerate(tsr_list, 1):
        numero_tsr = tsr.get('tsr', 'N/A')
        titulo = tsr.get('titulo', 'Sin título')
        
        print(f"\n📚 [{i}/{len(tsr_list)}] TSR{numero_tsr}: {titulo}")
        print(f"   📖 Fuentes: {len(tsr.get('fuentes', []))}")
        
        # Generar resumen
        resultado = generar_resumen(tsr)
        
        if resultado['exito']:
            print(f"   ✅ {resultado['num_palabras']} palabras")
            
            resultados.append({
                "tsr": numero_tsr,
                "titulo": titulo,
                "cluster": tsr.get('cluster', 'Sin cluster'),
                "resumen": resultado['resumen'],
                "num_palabras": resultado['num_palabras'],
                "num_fuentes_usadas": len(tsr.get('fuentes', [])),
                "fecha_generacion": datetime.now().isoformat()
            })
            
            exitosos += 1
        else:
            print(f"   ❌ Error: {resultado.get('error', 'Desconocido')}")
            fallidos += 1
        
        # Delay
        if i < len(tsr_list):
            print(f"   ⏳ Pausa {DELAY_SEGUNDOS}s...")
            time.sleep(DELAY_SEGUNDOS)
    
    # ========================================================================
    # GUARDAR
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("💾 GUARDANDO")
    print("=" * 80)
    
    total_palabras = sum(r['num_palabras'] for r in resultados)
    promedio = total_palabras / len(resultados) if resultados else 0
    
    datos_salida = {
        "metadata": {
            "capa": "CAPA 2: Resúmenes Conceptuales",
            "fecha_generacion": datetime.now().isoformat(),
            "total_tsr": len(resultados),
            "exitosos": exitosos,
            "fallidos": fallidos,
            "tasa_exito": f"{(exitosos/len(tsr_list)*100):.1f}%",
            "total_palabras": total_palabras,
            "promedio_palabras_tsr": round(promedio, 1),
            "modelo": MODELO,
            "archivo_origen": ARCHIVO_ENTRADA
        },
        "resultados": resultados
    }
    
    with open(ARCHIVO_SALIDA, 'w', encoding='utf-8') as f:
        json.dump(datos_salida, f, indent=2, ensure_ascii=False)
    
    # ========================================================================
    # RESUMEN
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("🎉 CAPA 2 COMPLETADA")
    print("=" * 80)
    print(f"\n📁 {ARCHIVO_SALIDA}")
    print(f"\n📊 Estadísticas:")
    print(f"   • TSRs procesados: {len(tsr_list)}")
    print(f"   • Exitosos: {exitosos}")
    print(f"   • Fallidos: {fallidos}")
    print(f"   • Tasa éxito: {(exitosos/len(tsr_list)*100):.1f}%")
    print(f"   • Palabras totales: {total_palabras:,}")
    print(f"   • Promedio: {promedio:.1f} palabras/TSR")
    print(f"   • Rango objetivo: 150-200 palabras")
    print("\n" + "=" * 80)
    print("✅ Listo para CAPA 3")
    print("=" * 80)


if __name__ == "__main__":
    main()
