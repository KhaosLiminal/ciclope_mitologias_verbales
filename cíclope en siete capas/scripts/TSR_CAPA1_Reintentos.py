"""
TSR_CAPA1_Reintentos.py - Script para reintentar TSRs fallidos
"""
import os
import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
import re
from dotenv import load_dotenv
from perplexity import Perplexity

# Cargar variables de entorno
load_dotenv()

# Configuración
MAX_REINTENTOS = 3
DELAY_INICIAL = 2  # segundos
FACTOR_BACKOFF = 2
MAX_DELAY = 60  # segundos

class TSRProcessor:
    def __init__(self):
        self.client = Perplexity(api_key=os.getenv("PERPLEXITY_API_KEY"))
        self.resultados_exitosos = []
        self.errores = []
        self.estadisticas = {
            "total_tsrs": 0,
            "tsrs_exitosos": 0,
            "tsrs_fallidos": 0,
            "fuentes_generadas": 0,
            "tiempo_inicio": datetime.now().isoformat()
        }

    def cargar_resultados_previos(self, ruta_resultados: str) -> List[Dict]:
        """Carga los resultados previos de un archivo JSON."""
        with open(ruta_resultados, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        return datos.get("resultados", [])

    def identificar_tsrs_fallidos(self, resultados_previos: List[Dict]) -> List[Dict]:
        """Identifica los TSRs que fallaron en la ejecución anterior."""
        return [tsr for tsr in resultados_previos if "error" in tsr or not tsr.get("fuentes")]

    def procesar_tsr_con_reintentos(self, tsr: Dict, max_reintentos: int = MAX_REINTENTOS) -> Dict:
        """Procesa un TSR con reintentos automáticos."""
        intentos = 0
        delay = DELAY_INICIAL

        while intentos < max_reintentos:
            try:
                resultado = self.generar_bibliografia_tsr(tsr)
                if resultado.get("fuentes"):
                    return resultado
            except Exception as e:
                print(f"   ⚠️  Intento {intentos + 1} fallido: {str(e)}")
                time.sleep(delay)
                delay = min(delay * FACTOR_BACKOFF, MAX_DELAY)
                intentos += 1

        return {
            **tsr,
            "error": f"Error después de {max_reintentos} intentos",
            "intentos": intentos,
            "fecha_error": datetime.now().isoformat()
        }

    def generar_bibliografia_tsr(self, tsr: Dict) -> Dict:
        """Genera la bibliografía para un TSR específico."""
        prompt = self._construir_prompt(tsr)
        respuesta = self._obtener_respuesta_api(prompt)
        return self._procesar_respuesta(respuesta, tsr)

    def _construir_prompt(self, tsr: Dict) -> str:
        """Construye el prompt para la API."""
        return f"""
        Genera una bibliografía académica para el TSR{tsr['numero']}:
        Título: {tsr['titulo']}
        Autor: {tsr['autor_primario']}
        Obra: {tsr['obra_primaria']}
        Año: {tsr['año']}
        Concepto central: {tsr['concepto_central']}
        """

    def _obtener_respuesta_api(self, prompt: str) -> str:
        """Obtiene la respuesta de la API de Perplexity."""
        response = self.client.search(
            query=prompt,
            max_results=5,
            max_tokens=2048
        )
        return response.results[0].content if response.results else ""

    def _procesar_respuesta(self, respuesta: str, tsr: Dict) -> Dict:
        """Procesa la respuesta de la API y extrae la bibliografía."""
        try:
            # Intenta extraer JSON de la respuesta
            bibliografia = self._extraer_json_respuesta(respuesta)
            return {
                **tsr,
                "fuentes": bibliografia,
                "fecha_generacion": datetime.now().isoformat(),
                "estado": "éxito"
            }
        except Exception as e:
            return {
                **tsr,
                "error": f"Error al procesar la respuesta: {str(e)}",
                "respuesta_cruda": respuesta,
                "fecha_error": datetime.now().isoformat()
            }

    def _extraer_json_respuesta(self, texto: str) -> List[Dict]:
        """Intenta extraer y validar JSON de la respuesta."""
        # Implementa la lógica de extracción de JSON aquí
        pass

    def guardar_resultados(self, ruta_salida: str):
        """Guarda los resultados en un archivo JSON."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_completa = os.path.join(ruta_salida, f"resultados_reintentos_{timestamp}.json")
        
        datos = {
            "metadata": {
                "fecha_generacion": datetime.now().isoformat(),
                "version": "1.0.0",
                "estadisticas": self.estadisticas
            },
            "resultados": self.resultados_exitosos + self.errores
        }

        with open(ruta_completa, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Resultados guardados en: {ruta_completa}")

def main():
    print("=" * 80)
    print("🔄 INICIANDO REINTENTOS DE TSRs FALLIDOS")
    print("=" * 80)

    # Configuración de rutas
    ruta_resultados = input("Ruta al archivo de resultados previos: ").strip('"')
    ruta_salida = input("Ruta para guardar los resultados (dejar vacío para 'resultados/'): ").strip('"') or "resultados"

    # Crear directorio de salida si no existe
    os.makedirs(ruta_salida, exist_ok=True)

    # Inicializar procesador
    procesador = TSRProcessor()

    try:
        # Cargar resultados previos
        resultados_previos = procesador.cargar_resultados_previos(ruta_resultados)
        tsrs_fallidos = procesador.identificar_tsrs_fallidos(resultados_previos)

        if not tsrs_fallidos:
            print("\n✅ No hay TSRs fallidos para reintentar.")
            return

        print(f"\n🔍 Se encontraron {len(tsrs_fallidos)} TSRs fallidos para reintentar.")

        # Procesar TSRs fallidos
        for i, tsr in enumerate(tsrs_fallidos, 1):
            print(f"\n🔄 Procesando TSR {tsr.get('numero')} ({i}/{len(tsrs_fallidos)})")
            resultado = procesador.procesar_tsr_con_reintentos(tsr)
            
            if "error" in resultado:
                print(f"   ❌ Error: {resultado['error']}")
                procesador.errores.append(resultado)
            else:
                print(f"   ✅ Éxito: {len(resultado.get('fuentes', []))} fuentes generadas")
                procesador.resultados_exitosos.append(resultado)

        # Actualizar estadísticas
        procesador.estadisticas.update({
            "total_tsrs": len(tsrs_fallidos),
            "tsrs_exitosos": len(procesador.resultados_exitosos),
            "tsrs_fallidos": len(procesador.errores),
            "fuentes_generadas": sum(len(tsr.get('fuentes', [])) for tsr in procesador.resultados_exitosos),
            "tiempo_fin": datetime.now().isoformat()
        })

        # Guardar resultados
        procesador.guardar_resultados(ruta_salida)

        # Mostrar resumen
        print("\n" + "=" * 80)
        print("📊 RESUMEN DE REINTENTOS")
        print("=" * 80)
        print(f"📅 Inicio: {procesador.estadisticas['tiempo_inicio']}")
        print(f"📅 Fin: {procesador.estadisticas['tiempo_fin']}")
        print(f"🔢 TSRs procesados: {procesador.estadisticas['total_tsrs']}")
        print(f"✅ Éxitos: {procesador.estadisticas['tsrs_exitosos']}")
        print(f"❌ Fallos: {procesador.estadisticas['tsrs_fallidos']}")
        print(f"📚 Fuentes generadas: {procesador.estadisticas['fuentes_generadas']}")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {str(e)}")
        if 'procesador' in locals():
            procesador.guardar_resultados(ruta_salida)
        raise

if __name__ == "__main__":
    main()