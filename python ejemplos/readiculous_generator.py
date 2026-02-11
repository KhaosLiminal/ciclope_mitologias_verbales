from perplexity import Perplexity

client = Perplexity(api_key="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")

# Prompt para generar 50 carteles filosóficos
prompt = """
Genera 50 estructuras de carteles filosóficos críticos sobre tecnología, ética, algoritmos, arte, capitalismo y sociedad digital.

Formato CSV estricto con 3 columnas: Titulo,Cuerpo,Quemadura

Reglas de condensación CRÍTICAS:
- Titulo: 5-7 palabras MÁXIMO, directo, provocador
- Cuerpo: 3-4 oraciones cortas, golpes conceptuales sin explicaciones
- Quemadura: 3 líneas filosas y memorables
- Sin saltos de línea dentro de celdas (todo en una línea por campo)
- Sin hashtags, links, ni números de cartel
- Sin comillas extras que rompan el CSV

Estilo: Irónico, crítico, filosóficamente denso pero condensado, más verdad y menos dato, lectura en segundo orden.

Temas obligatorios (distribuir entre los 50):
- Ética con IA
- Deseo domesticado y consumo algorítmico
- Libertad vs control digital
- Identidad fragmentada en redes
- Capitalismo de vigilancia
- Resistencia y obediencia
- Naturaleza vs tecnología
- Futuro automatizado
- Democracia algorítmica
- Arte e inteligencia artificial
- Memoria y archivo digital

Ejemplo de formato correcto:
Titulo,Cuerpo,Quemadura
Deseo domesticado,Tu deseo llegó por Amazon Prime. Antes el deseo era peligroso: deseabas salida transformación poder. Ahora deseas lo que el algoritmo desea que desees.,Es más limpio. Menos revolucionario. Más rentable.

Genera EXACTAMENTE 50 filas incluyendo el header. Responde SOLO con el CSV, sin texto adicional.
"""

# Búsqueda con el prompt
search = client.search.create(
    query=prompt,
    max_results=1,  # Solo necesitamos la generación
    max_tokens_per_page=8192  # Suficiente para 50 carteles
)

# Extraer el resultado
if search.results:
    csv_content = search.results[0].snippet
    
    # Guardar CSV
    with open("readiculous_50_carteles_itera.csv", "w", encoding="utf-8") as f:
        f.write(csv_content)
    
    print("✅ CSV generado: readiculous_50_carteles_itera.csv")
    print(f"📊 Primeras líneas:\n{csv_content[:500]}...")
else:
    print("❌ No se generaron resultados")
