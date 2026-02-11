from perplexity import Perplexity

client = Perplexity()

# Usar el endpoint de CHAT para generación
messages = [
    {
        "role": "system",
        "content": "Eres un filósofo crítico especializado en teoría de los medios, capitalismo de vigilancia y crítica cultural. Tu estilo es denso, irónico y provocador como Guy Debord encuentra a Twitter."
    },
    {
        "role": "user",
        "content": """
Genera EXACTAMENTE 50 carteles críticos en formato CSV.

Formato: Titulo,Cuerpo,Quemadura

Reglas estrictas:
- Titulo: 5-7 palabras máximo
- Cuerpo: 2-3 oraciones cortas, sin explicaciones
- Quemadura: 1 línea filosa
- Sin saltos de línea en celdas
- Sin hashtags, links, números

Temas: algoritmos, deseo, consumo, libertad, identidad digital, capitalismo vigilancia, resistencia, naturaleza vs tech, futuro, democracia, arte AI, memoria digital

Ejemplo:
Titulo,Cuerpo,Quemadura
Deseo domesticado,Tu deseo llegó por Amazon Prime. Antes el deseo era peligroso: deseabas salida transformación poder. Ahora deseas lo que el algoritmo desea que desees.,Es más limpio. Menos revolucionario. Más rentable.

Responde SOLO con el CSV sin texto adicional.
"""
    }
]

# Llamada al endpoint de chat
try:
    response = client.chat.completions.create(
        model="sonar-pro",  # Modelo más potente
        messages=messages
    )
    
    csv_content = response.choices[0].message.content
    
    # Guardar CSV
    with open("readiculous_50_carteles.csv", "w", encoding="utf-8") as f:
        f.write(csv_content)
    
    print("✅ CSV generado: readiculous_50_carteles.csv")
    print(f"📊 Primeras líneas:\n{csv_content[:300]}...")
    
except AttributeError:
    print("❌ El SDK no tiene el método chat.completions")
    print("📖 Verifica la documentación del API en:")
    print("https://docs.perplexity.ai/api-reference/chat-completions")

