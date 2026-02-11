# scripts/ejecutar_capa1.py
"""
Script principal para ejecutar la generación de la Capa 1 (Bibliografía Verificada).
Incluye manejo de errores, reintentos y generación de reportes.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Agregar el directorio raíz al path para importaciones
sys.path.append(str(Path(__file__).parent.parent))

from src.api_client import PerplexityClient
from src.models import TSRMetadata, FuenteBibliografica, ResultadoTSR, EstadisticasEjecucion
from src.validators import validar_estructura_fuente, extraer_json_respuesta
from src.utils import (
    cargar_tsrs_desde_archivo,
    guardar_resultados,
    limpiar_texto,
    crear_directorio_si_no_existe
)

# Configuración
MAX_REINTENTOS = 3
DELAY_INICIAL = 2  # segundos
FACTOR_BACKOFF = 2
MAX_DELAY = 60  # segundos

def main():
    """Función principal para ejecutar la generación de la Capa 1."""
    try:
        print("=" * 80)
        print("🚀 INICIANDO GENERACIÓN DE CAPA 1 - BIBLIOGRAFÍA VERIFICADA")
        print("=" * 80)
        
        # Inicializar cliente de Perplexity
        client = PerplexityClient()
        
        # Cargar metadatos de TSRs
        ruta_metadatos = Path("datos/tsr_metadatos.json")
        if not ruta_metadatos.exists():
            print(f"❌ Error: No se encontró el archivo de metadatos en {ruta_metadatos}")
            return
            
        tsrs = cargar_tsrs_desde_archivo(ruta_metadatos)
        print(f"📚 Se cargaron {len(tsrs)} TSRs para procesar")
        
        # Directorios de salida
        directorio_salida = Path("resultados")
        directorio_debug = directorio_salida / "debug"
        crear_directorio_si_no_existe(directorio_salida)
        crear_directorio_si_no_existe(directorio_debug)
        
        # Inicializar estadísticas
        estadisticas = EstadisticasEjecucion(
            total_tsrs=len(tsrs),
            tsrs_exitosos=0,
            tsrs_fallidos=0,
            fuentes_generadas=0,
            tiempo_inicio=datetime.now()
        )
        
        # Procesar cada TSR
        resultados = []
        for tsr in tsrs:
            print(f"\n🔍 Procesando TSR{tsr.numero}: {tsr.titulo}")
            
            # Intentar generar la bibliografía con reintentos
            resultado = procesar_tsr_con_reintentos(client, tsr, MAX_REINTENTOS)
            
            # Actualizar estadísticas
            if resultado.exito:
                estadisticas.tsrs_exitosos += 1
                estadisticas.fuentes_generadas += len(resultado.fuentes)
                print(f"   ✅ Éxito: {len(resultado.fuentes)} fuentes generadas")
            else:
                estadisticas.tsrs_fallidos += 1
                print(f"   ❌ Fallo: {resultado.error}")
                
            resultados.append(resultado)
            
            # Guardar resultados parciales
            if len(resultados) % 5 == 0:
                guardar_resultados_parciales(resultados, directorio_salida)
        
        # Guardar resultados finales
        guardar_resultados_finales(resultados, directorio_salida, estadisticas)
        
        # Mostrar resumen
        mostrar_resumen_ejecucion(estadisticas)
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {str(e)}")
        sys.exit(1)

def procesar_tsr_con_reintentos(
    client: PerplexityClient,
    tsr: TSRMetadata,
    max_reintentos: int
) -> ResultadoTSR:
    """
    Procesa un TSR con reintentos en caso de fallos.
    
    Args:
        client: Cliente de Perplexity
        tsr: Metadatos del TSR a procesar
        max_reintentos: Número máximo de reintentos
        
    Returns:
        Resultado del procesamiento del TSR
    """
    # Implementación de la lógica de reintentos
    pass

def guardar_resultados_parciales(
    resultados: List[ResultadoTSR],
    directorio_salida: Path
) -> None:
    """Guarda resultados parciales durante la ejecución."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_parcial = directorio_salida / f"resultados_parciales_{timestamp}.json"
    
    with open(ruta_parcial, "w", encoding="utf-8") as f:
        json.dump([r.dict() for r in resultados], f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados parciales guardados en {ruta_parcial}")

def guardar_resultados_finales(
    resultados: List[ResultadoTSR],
    directorio_salida: Path,
    estadisticas: EstadisticasEjecucion
) -> None:
    """Guarda los resultados finales de la ejecución."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_final = directorio_salida / f"resultados_finales_{timestamp}.json"
    
    datos_salida = {
        "metadata": {
            "fecha_generacion": datetime.now().isoformat(),
            "version": "1.0.0",
            "estadisticas": estadisticas.dict()
        },
        "resultados": [r.dict() for r in resultados]
    }
    
    with open(ruta_final, "w", encoding="utf-8") as f:
        json.dump(datos_salida, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados finales guardados en {ruta_final}")

def mostrar_resumen_ejecucion(estadisticas: EstadisticasEjecucion) -> None:
    """Muestra un resumen de la ejecución."""
    duracion = (datetime.now() - estadisticas.tiempo_inicio).total_seconds() / 60
    
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE EJECUCIÓN")
    print("=" * 80)
    print(f"📅 Inicio: {estadisticas.tiempo_inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱️  Duración: {duracion:.2f} minutos")
    print(f"✅ TSRs exitosos: {estadisticas.tsrs_exitosos}/{estadisticas.total_tsrs}")
    print(f"❌ TSRs fallidos: {estadisticas.tsrs_fallidos}/{estadisticas.total_tsrs}")
    print(f"📚 Fuentes generadas: {estadisticas.fuentes_generadas}")
    print(f"📊 Tasa de éxito: {estadisticas.tasa_exito():.1f}%")
    print("=" * 80)

if __name__ == "__main__":
    main()