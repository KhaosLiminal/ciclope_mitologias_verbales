from perplexity import Perplexity

client = Perplexity()

# MISMO prompt exacto
prompt = """
Analiza cómo la lengua spanglish de quienes cruzan la frontera se manifiesta 
en estructuras contemporáneas (algoritmos, plataformas, biopolítica computacional) 
con rigor conceptual.

Después de tu análisis, genera 150 carteles políticos en spanglish críticos en formato CSV:
Titulo,Cuerpo,Quemadura

Con estas reglas:
- Titulo: 3-5 palabras spanglish, conceptualmente denso
- Cuerpo: 6-7 oraciones spanglish densas, vivencia crítica pura
- Quemadura: 2-3 línea filosóficamente densa

Temas: calles, trabajo, espectáculo integrado, amor, dolor, reificación digital, gratitud,
subsunción algorítmica, poesía, devoción, albur, totalitarismo sin sujeto, nostalgia, biopolítica computacional, 
migración, gastronomía, malestar de la cultura, México profundo y eterno, pedagogía del oprimido
"""

# SIN búsqueda web - FORZADO a usar solo training data
completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "Eres un filósofo mexicano crítico radicalizado en los Estados Unidos."},
        {"role": "user", "content": prompt}
    ],
    model="sonar-pro",
    temperature=0.7,
    max_tokens=4000,
    disable_search=True  # ← CRÍTICO: Sin búsqueda web
)

print("="*70)
print("🚫 AMERICA PARA LOS AMERICANOS: SIN BÚSQUEDA WEB (disable_search=True)")
print(f"🤖 Modelo: {completion.model}")
print(f"📊 Tokens: {completion.usage.total_tokens}")
print("="*70)
print("\n📄 RESPUESTA:\n")
print(completion.choices[0].message.content)
print("\n" + "="*70)

# Guardar resultado
with open("la_frontera_me_cruzó.txt", "w", encoding="utf-8") as f:
    f.write(completion.choices[0].message.content)

print("\n✅ Resultado guardado en: debord_sin_busqueda.txt")
