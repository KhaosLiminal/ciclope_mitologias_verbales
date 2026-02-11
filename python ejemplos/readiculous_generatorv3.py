from perplexity import Perplexity

client = Perplexity()

# Mensaje del sistema para establecer el comportamiento
system_prompt = """Eres un filósofo crítico especializado en teoría de los medios, capitalismo de vigilancia y crítica cultural. Tu estilo es denso, irónico y provocador como Guy Debord encuentra a Twitter. 

Genera SOLO el contenido CSV solicitado sin texto adicional, sin búsquedas web, sin referencias a fuentes externas."""

# Prompt del usuario
user_prompt = """
Genera EXACTAMENTE 50 carteles críticos en formato CSV.

Formato estricto:
Titulo,Cuerpo,Quemadura

Reglas:
- Titulo: 5-7 palabras máximo, directo, provocador
- Cuerpo: 2-3 oraciones cortas, sin explicaciones
- Quemadura: 1 línea filosa y memorable
- Sin saltos de línea en celdas
- Sin hashtags, links, números
- Sin buscar información web

Temas: algoritmos, deseo domesticado, consumo, libertad digital, identidad, capitalismo vigilancia, resistencia, naturaleza vs tech, futuro automatizado, democracia algorítmica, arte AI, memoria digital

Ejemplo de UNA fila:
Deseo domesticado,Tu deseo llegó por Amazon Prime. Antes el deseo era peligroso: deseabas salida transformación poder. Ahora deseas lo que el algoritmo desea que desees.,Es más limpio. Menos revolucionario. Más rentable.

Genera las 50 filas (más header) AHORA.
"""

# Crear completion SIN búsqueda web
completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    model="sonar-pro",  # Modelo más potente
    temperature=0.8,  # Alta creatividad
    max_tokens=4000,  # Suficiente para 50 carteles
    # NO incluir web_search_options para evitar búsquedas web
)

# Extraer respuesta
csv_content = completion.choices[0].message.content

# Guardar CSV
with open("readiculous_50_carteles.csv", "w", encoding="utf-8") as f:
    f.write(csv_content)

print("✅ CSV generado: readiculous_50_carteles.csv")
print(f"📊 Primeras 500 caracteres:")
print(csv_content[:500])
print("\n...")
print(f"📊 Últimas 300 caracteres:")
print(csv_content[-300:])
