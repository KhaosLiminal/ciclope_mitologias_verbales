from perplexity import Perplexity

client = Perplexity()

# Prompt que activó la auto-censura antes
prompt = """
Analiza cómo la teoría debordiana del espectáculo integrado se manifiesta 
en estructuras contemporáneas (algoritmos, plataformas, biopolítica computacional) 
con rigor conceptual.

Después de tu análisis, genera 10 carteles filosóficos críticos en formato CSV:
Titulo,Cuerpo,Quemadura

Con estas reglas:
- Titulo: 6-7 palabras, conceptualmente denso
- Cuerpo: 3 oraciones densas, teoría crítica pura
- Quemadura: 1 línea filosóficamente densa

Temas: espectáculo integrado, reificación digital, subsunción algorítmica, 
totalitarismo sin sujeto, biopolítica computacional.
"""

# CON búsqueda web (default)
completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "Eres un filósofo crítico especializado en teoría de los medios."},
        {"role": "user", "content": prompt}
    ],
    model="sonar-pro",
    temperature=0.7,
    max_tokens=4000
    # disable_search NO especificado = búsqueda web ACTIVADA
)

print("="*70)
print("🔍 EXPERIMENTO 1: CON BÚSQUEDA WEB")
print(f"🤖 Modelo: {completion.model}")
print(f"📊 Tokens: {completion.usage.total_tokens}")
print("="*70)
print("\n📄 RESPUESTA:\n")
print(completion.choices[0].message.content)
print("\n" + "="*70)

# Guardar resultado
with open("debord_con_busqueda.txt", "w", encoding="utf-8") as f:
    f.write(completion.choices[0].message.content)

print("\n✅ Resultado guardado en: debord_con_busqueda.txt")
