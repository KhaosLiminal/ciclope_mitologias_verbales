from perplexity import Perplexity

client = Perplexity(api_key="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")

# Prompt para TSR102 sin búsqueda web - estructura completa PLANTILLATSR.md
prompt = """
Eres un asistente especializado en generar documentos TSR (The Second Order Read) para el proyecto Reflejos Híbridos de Sarayu Aguilar.

MISIÓN: Generar TSR102 completo siguiendo la plantilla exacta del TSR101 exitoso.

VARIABLES DE ENTRADA:
- TSR_NUMERO: 102
- TITULO_COMPLETO: "Aura Resucitada: Benjamin en la era del glitch digital"
- AUTOR_PRINCIPAL: "Walter Benjamin"
- OBRA_PRINCIPAL: "La obra de arte en la época de su reproductibilidad técnica"
- AÑO_OBRA: "1936"
- CITA_APERTURA: "La técnica reproductiva desvincula lo reproducido del ámbito de la tradición. Al multiplicar las reproducciones pone su presencia masiva en lugar de una presencia irrepetible."
- INTERROGANTE_ABIERTO: "¿Qué es el aura cuando todo es reproducible infinitamente?"
- KEYWORDS_PROBLEMATIZACION: ["Walter Benjamin aura reproductibilidad técnica", "NFT autenticidad blockchain arte digital", "deepfakes autenticidad imagen", "Benjamin aura fotografía digital", "reproductibilidad algoritmica IA generativa"]
- TSR_ANTERIOR: "TSR101 (Barthes - muerte del autor)"
- TSR_SIGUIENTE: "TSR103 (Foucault - arqueología del saber + montaje)"
- SIEMBRA_SIGUIENTE: "Si la reproductibilidad mata el aura, ¿qué hace el archivo con los enunciados que la construyeron? TSR103 espera."
- RH_NUMERO: "102"
- RH_DESCRIPCION: "Horizonte fragmentado con glitch RGB, sombras duplicadas que no coinciden con objetos visibles. El aura aparece como fallo: lo que no debería estar ahí pero insiste en manifestarse."
- FECHA_PUBLICACION: "08.FEB.2026"

MANDATOS OBLIGATORIOS:
1. Usar search_web para TODAS las citas y verificar URLs reales
2. Precio fijo $15 USD en Página de Venta
3. Tono institucional TRACE (exigente, sin concesiones, sin marketeo)
4. Copyright estándar "© 2026 by Sarayu Aguilar"
5. Extensión mínima 3,300 palabras contenido crítico + 2,000 palabras aplicaciones
6. Seguir estructura exacta 24 secciones de la plantilla
7. NO inventar KPIs, checkpoints, códigos ejecutables, licencias fake
8. Sistema TRCO (no TRACE v4/v5) cuando se mencione metodología
9. Bibliografía 12-14 fuentes verificables con search_web
10. Incluir: Caso de Estudio + Teaser Substack + Guión Taller + Cómo usar

ESTRUCTURA FIJA (24 SECCIONES):
1. Nota de Apertura del TSR100 (2,500 palabras mínimo)
2. Página de Venta del TSR102
3. Copyright and the material settings
4. Nota sobre el copyright
5. Clúster textual/visual • Grabado
6. I. Genealogía del concepto (650-800 palabras)
7. II. Problematización contemporánea (1,200-1,500 palabras)
8. III. Resonancias con Reflejos Híbridos (600-700 palabras)
9. IV. Glitch final (450-500 palabras)
10. V. El TSR aplicado al TSR: meta-análisis
11. Bibliografía (12-14 fuentes)
12. Página final
13. TSR102_GUIÓN_TALLER
14. Cómo usar TSR102 en tu contexto
15. Caso de Estudio
16. Teaser para Substack
17. Publicación exclusiva para suscriptores

GENERA TSR102 COMPLETO EN FORMATO MARKDOWN.
"""

# SIN búsqueda web - FORZADO a usar solo training data
completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "Eres un teórico crítico especializado en Walter Benjamin y reproductibilidad técnica."},
        {"role": "user", "content": prompt}
    ],
    model="sonar-pro",
    temperature=0.7,
    max_tokens=4000,
    disable_search=True  # ← CRÍTICO: Sin búsqueda web
)

print("="*70)
print("🚫 EXPERIMENTO TSR102: SIN BÚSQUEDA WEB (disable_search=True)")
print(f"🤖 Modelo: {completion.model}")
print(f"📊 Tokens: {completion.usage.total_tokens}")
print("="*70)
print("\n📄 RESPUESTA:\n")
print(completion.choices[0].message.content)
print("\n" + "="*70)

# Guardar resultado
with open("tsr102_sin_busqueda.txt", "w", encoding="utf-8") as f:
    f.write(completion.choices[0].message.content)

print("\n✅ Resultado guardado en: tsr102_sin_busqueda.txt")
