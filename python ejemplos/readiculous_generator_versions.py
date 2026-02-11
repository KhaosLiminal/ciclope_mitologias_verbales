from perplexity import Perplexity

client = Perplexity()

# Definir 3 niveles de densidad
versions = {
    "light": {
        "name": "Versión Viral (Instagram/TikTok friendly)",
        "temperature": 0.9,
        "system_prompt": """Eres un comunicador crítico que hace filosofía accesible sin perder el filo. 
        Tu estilo es irónico pero ligero, punzante pero breve. Como memes filosóficos que el algoritmo tolera.""",
        "user_prompt": """
Genera 50 carteles críticos LIGEROS y VIRALES para redes sociales.

Formato: Titulo,Cuerpo,Quemadura

Reglas especiales para alcance algorítmico:
- Titulo: 4-5 palabras MAX, directo, memorable
- Cuerpo: 1-2 oraciones CORTAS (máximo 15 palabras cada una), golpe conceptual inmediato
- Quemadura: 1 línea ultra-corta (5-8 palabras), memorable como eslogan
- Lenguaje accesible sin perder ironía
- Tono: Irónico pero no denso, crítico pero compartible

Temas: algoritmos, redes sociales, likes, identidad digital, consumo online, selfies, stories, viralidad

Ejemplo:
Tu like es tu voto,Cada corazón alimenta la máquina. El engagement es tu trabajo gratis.,Trabajas para el algoritmo sin saberlo.
        """
    },
    
    "medium": {
        "name": "Versión Balanceada (Twitter/Threads)",
        "temperature": 0.8,
        "system_prompt": """Eres un pensador crítico con estilo periodístico filosófico. 
        Balanceas profundidad con legibilidad. Como artículos de The Atlantic pero condensados en tweets.""",
        "user_prompt": """
Genera 50 carteles críticos BALANCEADOS entre profundidad y accesibilidad.

Formato: Titulo,Cuerpo,Quemadura

Reglas:
- Titulo: 5-6 palabras, provocador pero claro
- Cuerpo: 2 oraciones medianas, conceptualmente denso pero legible
- Quemadura: 1 línea memorable (8-12 palabras)
- Lenguaje: Filosófico pero comprensible sin glosario

Temas: capitalismo digital, vigilancia, deseo algorítmico, libertad vs control, identidad fragmentada

Ejemplo:
Libertad de elegir entre jaulas,Mil opciones te esperan en la pantalla. Todas conducen al mismo lugar.,El algoritmo diseñó todas tus opciones.
        """
    },
    
    "heavy": {
        "name": "Versión Densa (Substack/Academia)",
        "temperature": 0.7,
        "system_prompt": """Eres un filósofo crítico especializado en teoría de los medios y capitalismo de vigilancia. 
        Tu estilo es denso, irónico y provocador como Guy Debord encuentra a Twitter. No concedes nada al algoritmo.""",
        "user_prompt": """
Genera 50 carteles críticos DENSOS y filosóficamente rigurosos.

Formato: Titulo,Cuerpo,Quemadura

Reglas:
- Titulo: 6-7 palabras, conceptualmente cargado
- Cuerpo: 3 oraciones densas, sin concesiones explicativas
- Quemadura: 1 línea filosóficamente densa y memorable
- Lenguaje: Teoría crítica pura, sin diluir

Temas: espectáculo integrado, reificación digital, subsunción algorítmica, totalitarismo sin sujeto, biopolítica computacional

Ejemplo:
Vigilancia sin vigilantes es perfección totalitaria,No hay enemigo. Solo hay lógica. No hay represión. Solo hay optimización.,El totalitarismo sin tirano es el futuro.
        """
    }
}

# Generar las 3 versiones
for version_key, config in versions.items():
    print(f"\n🔄 Generando {config['name']}...")
    
    completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": config["system_prompt"]},
            {"role": "user", "content": config["user_prompt"]}
        ],
        model="sonar-pro",
        temperature=config["temperature"],
        max_tokens=4000
    )
    
    # Extraer modelo usado y estadísticas
    csv_content = completion.choices[0].message.content
    model_used = completion.model  # Modelo real usado
    usage = completion.usage       # Estadísticas de uso
    
    # Guardar con nombre diferente
    filename = f"readiculous_50_{version_key}.csv"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(csv_content)
    
    print(f"✅ {config['name']} guardado: {filename}")
    print(f"🤖 Modelo real usado: {model_used}")
    print(f"📊 Tokens usados: {usage.prompt_tokens} entrada, {usage.completion_tokens} salida")
    print(f"📊 Preview:")
    print(csv_content[:300])
    print("...\n")

print("\n🎉 3 versiones generadas:")
print("📱 readiculous_50_light.csv → Instagram/TikTok (Algoritmo feliz)")
print("🐦 readiculous_50_medium.csv → Twitter/Threads (Balance)")
print("📚 readiculous_50_heavy.csv → Substack/Academia (Fuck el algoritmo)")
