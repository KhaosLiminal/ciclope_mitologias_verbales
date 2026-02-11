from perplexity import Perplexity
import json
from datetime import datetime
import os

# ← PEGÁ TU API KEY ACÁ (o ya la tenés configurada en variables de entorno)
# os.environ['PERPLEXITY_API_KEY'] = 'pplx-xxxxxxxxxxxxx'

client = Perplexity()

# ARQUITECTURA COMPLETA: 19 TSR en 7 clústeres
TSR_METADATA = [
    # CLÚSTER I: AUTORÍA, ESCRITURA, FRAGMENTO (4 TSR)
    {
        "numero": "102",
        "cluster": "I. Autoría, Escritura, Fragmento",
        "titulo": "Foucault: la verdad como archivo de enunciados",
        "autor_primario": "Michel Foucault",
        "obra_primaria": "¿Qué es un autor?",
        "año": 1969,
        "concepto_central": "función-autor",
        "keywords": ["autor como función", "enunciado", "episteme", "arqueología del saber", "condiciones de existencia discursiva"],
        "autores_secundarios": ["Roland Barthes", "Umberto Eco"],
        "conexion_RH": "IA generativa y autoría algorítmica",
        "glitch_conceptual": "El autor no desaparece: se convierte en función que opera desde la sombra"
    },
    {
        "numero": "103",
        "cluster": "I. Autoría, Escritura, Fragmento",
        "titulo": "Blanchot: el fragmento sin promesa de totalidad",
        "autor_primario": "Maurice Blanchot",
        "obra_primaria": "El espacio literario",
        "año": 1955,
        "concepto_central": "desaparición hablante del autor",
        "keywords": ["fragmento", "espacio literario", "inacabamiento radical", "intimidad escritura-lectura", "ausencia presencia"],
        "autores_secundarios": ["Friedrich Schlegel", "Roland Barthes"],
        "conexion_RH": "LLMs que completan frases: ¿quién habla cuando el modelo continúa?",
        "glitch_conceptual": "La obra habita un espacio donde no hay origen, solo presencia ausente"
    },
    {
        "numero": "104",
        "cluster": "I. Autoría, Escritura, Fragmento",
        "titulo": "El fragmento romántico como infinito concentrado",
        "autor_primario": "Friedrich Schlegel",
        "obra_primaria": "Fragmentos del Athenäum",
        "año": 1797,
        "concepto_central": "fragmento como totalidad",
        "keywords": ["romanticismo alemán", "fragmento", "totalidad", "infinito", "perspectiva condensada"],
        "autores_secundarios": ["Novalis", "Maurice Blanchot"],
        "conexion_RH": "Posts en redes como fragmentos que prometen totalidad inexistente",
        "glitch_conceptual": "El fragmento no es parte de nada: es la forma misma de lo ilimitado"
    },
    {
        "numero": "105",
        "cluster": "I. Autoría, Escritura, Fragmento",
        "titulo": "Blanchot contra Schlegel: la brecha irresoluble",
        "autor_primario": "Maurice Blanchot",
        "obra_primaria": "La escritura del desastre",
        "año": 1980,
        "concepto_central": "fragmento sin síntesis",
        "keywords": ["crítica del romanticismo", "brecha irresoluble", "imposibilidad de totalidad", "después del todo"],
        "autores_secundarios": ["Friedrich Schlegel", "Emmanuel Levinas"],
        "conexion_RH": "Escritura colaborativa humano-IA: ¿converge o fractura?",
        "glitch_conceptual": "Romanticismo = esperanza de síntesis. Blanchot = aceptación de la brecha irresoluble"
    },
    
    # CLÚSTER II: PIGMENTOS, COLOR, MERCADO, PODER (5 TSR)
    {
        "numero": "106",
        "cluster": "II. Pigmentos, Color, Mercado, Poder",
        "titulo": "Colores como botín teológico",
        "autor_primario": "Victoria Finlay",
        "obra_primaria": "Color: A Natural History of the Palette",
        "año": 2002,
        "concepto_central": "economía política del color",
        "keywords": ["lapislázuli", "ultramarino", "cochinilla", "comercio medieval", "teología del mercado"],
        "autores_secundarios": ["Michel Pastoureau", "Anne Varichon"],
        "conexion_RH": "Paletas de color en diseño digital: ¿acceso universal o uniformización?",
        "glitch_conceptual": "El color es código. La escasez es teología. El mercado es liturgia"
    },
    {
        "numero": "107",
        "cluster": "II. Pigmentos, Color, Mercado, Poder",
        "titulo": "El azul sintético como democratización o pérdida de aura",
        "autor_primario": "Walter Benjamin",
        "obra_primaria": "La obra de arte en la época de su reproductibilidad técnica",
        "año": 1936,
        "concepto_central": "aura y reproducción técnica",
        "keywords": ["Jean Baptiste Guimet", "ultramarino sintético", "democratización del arte", "pérdida de aura", "mercado pigmentos"],
        "autores_secundarios": ["Victoria Finlay", "Michel Pastoureau"],
        "conexion_RH": "Filtros de Instagram: democratización estética o estandarización visual",
        "glitch_conceptual": "¿Se liberó el arte o perdió el color su aura sagrada?"
    },
    {
        "numero": "108",
        "cluster": "II. Pigmentos, Color, Mercado, Poder",
        "titulo": "Eco: no hay lectura sin cultura",
        "autor_primario": "Umberto Eco",
        "obra_primaria": "Tratado de semiótica general",
        "año": 1976,
        "concepto_central": "signo como convención cultural",
        "keywords": ["semiótica", "significado cultural", "convención", "lectura neutral imposible", "código compartido"],
        "autores_secundarios": ["Charles Sanders Peirce", "Ferdinand de Saussure"],
        "conexion_RH": "Sesgo cultural en datasets de IA: no hay modelo neutral",
        "glitch_conceptual": "No existe significado sin cultura. No existe lectura neutral"
    },
    {
        "numero": "109",
        "cluster": "II. Pigmentos, Color, Mercado, Poder",
        "titulo": "Klein: el vacío azul como apropiación inmaterial",
        "autor_primario": "Yves Klein",
        "obra_primaria": "El vacío (Le Vide, exposición 1958)",
        "año": 1958,
        "concepto_central": "inmaterialidad artística",
        "keywords": ["IKB", "International Klein Blue", "monocromo", "zona de inmaterialidad", "oro ritual"],
        "autores_secundarios": ["Pierre Restany", "Gaston Bachelard"],
        "conexion_RH": "NFTs: propiedad de lo inmaterial o especulación vacía",
        "glitch_conceptual": "Klein no pintaba color: pintaba ausencia"
    },
    {
        "numero": "110",
        "cluster": "II. Pigmentos, Color, Mercado, Poder",
        "titulo": "El color como ventana mística",
        "autor_primario": "Yves Klein",
        "obra_primaria": "Anthropométries (serie 1960)",
        "año": 1960,
        "concepto_central": "experiencia mística del color",
        "keywords": ["monocromo", "experiencia perceptual", "disolución sujeto-objeto", "océano azul", "estado alterado"],
        "autores_secundarios": ["Mark Rothko", "Wassily Kandinsky"],
        "conexion_RH": "Pantallas LED: ¿el aura sobrevive a la digitalización?",
        "glitch_conceptual": "¿El aura sobrevive cuando el color se vuelve píxel?"
    },
    
    # CLÚSTER III: ORIGEN DE LA ESCRITURA (2 TSR)
    {
        "numero": "111",
        "cluster": "III. Origen de la Escritura",
        "titulo": "Escritura nacida del inventario",
        "autor_primario": "Denise Schmandt-Besserat",
        "obra_primaria": "Before Writing: From Counting to Cuneiform",
        "año": 1992,
        "concepto_central": "escritura como contabilidad",
        "keywords": ["cuneiforme", "Mesopotamia", "fichas de arcilla", "contabilidad", "control económico"],
        "autores_secundarios": ["Jean Bottéro", "Jack Goody"],
        "conexion_RH": "Blockchain como escritura contable distribuida",
        "glitch_conceptual": "El primer acto de civilización es el control económico"
    },
    {
        "numero": "112",
        "cluster": "III. Origen de la Escritura",
        "titulo": "Tablilla vs. papiro: la tecnología como episteme",
        "autor_primario": "Jack Goody",
        "obra_primaria": "The Logic of Writing and the Organization of Society",
        "año": 1986,
        "concepto_central": "materialidad del soporte",
        "keywords": ["tablilla arcilla", "papiro", "durabilidad", "tecnología soporte", "archivo histórico"],
        "autores_secundarios": ["Friedrich Kittler", "Marshall McLuhan"],
        "conexion_RH": "Almacenamiento en la nube: ¿archivo permanente o amnesia programada?",
        "glitch_conceptual": "Leemos los residuos, no la verdad"
    },
    
    # CLÚSTER IV: SEMIÓTICA, INTERPRETACIÓN, CRÍTICA (3 TSR)
    {
        "numero": "113",
        "cluster": "IV. Semiótica, Interpretación, Crítica",
        "titulo": "Leer como apropiación, no como obediencia",
        "autor_primario": "Roger Chartier",
        "obra_primaria": "El orden de los libros",
        "año": 1992,
        "concepto_central": "prácticas de lectura",
        "keywords": ["historia de la lectura", "apropiación", "protocolos lectura", "materialidad del libro", "sabotaje popular"],
        "autores_secundarios": ["Michel de Certeau", "Pierre Bourdieu"],
        "conexion_RH": "Lectura en pantalla vs. papel: ¿misma experiencia o episteme distinta?",
        "glitch_conceptual": "Todo texto es campo de batalla, no mandato"
    },
    {
        "numero": "114",
        "cluster": "IV. Semiótica, Interpretación, Crítica",
        "titulo": "Foucault: la verdad como archivo de enunciados",
        "autor_primario": "Michel Foucault",
        "obra_primaria": "La arqueología del saber",
        "año": 1969,
        "concepto_central": "arqueología del saber",
        "keywords": ["enunciado", "formación discursiva", "episteme", "condiciones de posibilidad", "poder-saber"],
        "autores_secundarios": ["Gilles Deleuze", "Georges Canguilhem"],
        "conexion_RH": "Arquitectura de prompts: ¿qué episteme habilitan los LLMs?",
        "glitch_conceptual": "El saber es cartografía de epistemas que habilitan lo decible"
    },
    {
        "numero": "115",
        "cluster": "IV. Semiótica, Interpretación, Crítica",
        "titulo": "Eiségesis: el error que somos",
        "autor_primario": "Hans-Georg Gadamer",
        "obra_primaria": "Verdad y método",
        "año": 1960,
        "concepto_central": "eiségesis vs. exégesis",
        "keywords": ["hermenéutica", "prejuicio", "proyección lectora", "círculo hermenéutico", "fusión de horizontes"],
        "autores_secundarios": ["Paul Ricoeur", "Umberto Eco"],
        "conexion_RH": "Personalización algorítmica: eiségesis como servicio",
        "glitch_conceptual": "¿No estamos institucionalizando la eiségesis como deseable?"
    },
    
    # CLÚSTER V: FRAGMENTO, AFORISMO, FORMA BREVE (2 TSR)
    {
        "numero": "116",
        "cluster": "V. Fragmento, Aforismo, Forma Breve",
        "titulo": "El aforismo como esqueleto del pensamiento",
        "autor_primario": "Javier Recas",
        "obra_primaria": "Teoría del aforismo (varios ensayos)",
        "año": 2010,
        "concepto_central": "aforismo como forma autónoma",
        "keywords": ["aforismo", "brevedad", "concisión", "esqueleto pensamiento", "incompletud sin culpa"],
        "autores_secundarios": ["Georg Christoph Lichtenberg", "Elias Canetti"],
        "conexion_RH": "Tweets filosóficos: aforismos o ruido informativo",
        "glitch_conceptual": "El aforismo no resume: condensa hasta la médula"
    },
    {
        "numero": "117",
        "cluster": "V. Fragmento, Aforismo, Forma Breve",
        "titulo": "Nietzsche: el aforismo como rebelión contra la totalidad",
        "autor_primario": "Friedrich Nietzsche",
        "obra_primaria": "Humano, demasiado humano",
        "año": 1878,
        "concepto_central": "aforismo como ruptura sistemática",
        "keywords": ["aforismo", "fragmento nietzscheano", "anti-sistema", "violencia sintáctica", "legibilidad futura"],
        "autores_secundarios": ["Arthur Schopenhauer", "Georg Simmel"],
        "conexion_RH": "Prompts como aforismos: ¿commodity o resistencia?",
        "glitch_conceptual": "Escribir en fragmentos es rebelión contra la totalidad"
    },
    
    # CLÚSTER VI: SEGUNDA ORDEN, PEDAGOGÍA, APRENDIZAJE (2 TSR)
    {
        "numero": "118",
        "cluster": "VI. Segunda Orden, Pedagogía, Aprendizaje",
        "titulo": "Freire: alfabetizar es desactivar el hechizo",
        "autor_primario": "Paulo Freire",
        "obra_primaria": "Pedagogía del oprimido",
        "año": 1970,
        "concepto_central": "alfabetización crítica",
        "keywords": ["pedagogía crítica", "conciencia crítica", "educación bancaria", "leer el mundo", "praxis liberadora"],
        "autores_secundarios": ["Ivan Illich", "bell hooks"],
        "conexion_RH": "Pedagogía de la IA: ¿crítica o reproductora?",
        "glitch_conceptual": "Leer palabras sin leer el mundo es domesticación"
    },
    {
        "numero": "119",
        "cluster": "VI. Segunda Orden, Pedagogía, Aprendizaje",
        "titulo": "Leer en voz alta: erotizar la sintaxis",
        "autor_primario": "Severo Sarduy",
        "obra_primaria": "Escrito sobre un cuerpo",
        "año": 1969,
        "concepto_central": "lectura como performance corporal",
        "keywords": ["voz alta", "materialidad vocal", "erotismo textual", "performance bucal", "cuerpo-texto"],
        "autores_secundarios": ["Roland Barthes", "Paul Zumthor"],
        "conexion_RH": "Voces sintéticas: ¿dónde queda el cuerpo en la lectura automática?",
        "glitch_conceptual": "Leer poesía en silencio es amputar una capa de sentido"
    },
    
    # CLÚSTER VII: AURA, REPRODUCCIÓN, TÉCNICA (1 TSR)
    {
        "numero": "120",
        "cluster": "VII. Aura, Reproducción, Técnica",
        "titulo": "Leer para dejar de ser el mismo",
        "autor_primario": "Roger Chartier",
        "obra_primaria": "Lecturas y lectores en la Francia del Antiguo Régimen",
        "año": 1987,
        "concepto_central": "lectura como transformación",
        "keywords": ["historia de la lectura", "prácticas lectoras", "transformación subjetiva", "apropiación textual", "riesgo hermenéutico"],
        "autores_secundarios": ["Paulo Freire", "Michel de Certeau"],
        "conexion_RH": "Lectura en IA: ¿consumo de información o transformación?",
        "glitch_conceptual": "Si cierras un texto siendo el mismo, no leíste: consumiste"
    }
]

# SYSTEM PROMPT para CAPA 1
SYSTEM_PROMPT_BIBLIOGRAFIA = """
Eres un investigador académico especializado en teoría crítica, filosofía continental, semiótica, historia del arte y pedagogía crítica del siglo XX-XXI.

Tu tarea es localizar y verificar fuentes bibliográficas rigurosas para investigación académica de alto nivel.

CRITERIOS DE CALIDAD:
1. Textos originales accesibles (PDFs de editoriales reconocidas, repositorios institucionales)
2. Análisis académicos recientes (2015-2026) que conecten teoría clásica con tecnología digital
3. Fuentes en español cuando sea posible (sin sacrificar calidad)
4. Diversidad de medios (libros, papers, conferencias académicas en video, tesis doctorales)
5. Priorizar fuentes con DOI o URL estable

DISTRIBUCIÓN OBLIGATORIA POR TSR:
- 40% teoría clásica (obras del autor primario + comentaristas canónicos)
- 30% teoría crítica relacionada (autores secundarios + diálogos conceptuales)
- 30% investigación contemporánea (papers 2020-2026 sobre IA/algoritmos/cultura digital)

VERIFICACIÓN:
- URL debe existir y ser accesible públicamente
- Evitar enlaces rotos, paywall sin alternativa, blogs sin respaldo institucional
- Si es video, debe ser académico (conferencias, clases universitarias, no divulgación superficial)

FORMATO DE RESPUESTA:
JSON estricto sin texto adicional antes ni después.
"""

# FUNCIÓN GENERADORA
def generar_bibliografia_tsr(tsr_data):
    """Genera bibliografía verificada para un TSR específico."""
    
    user_prompt = f"""
Busca y verifica 12-14 fuentes académicas para el TSR{tsr_data['numero']}.

METADATA DEL TSR:
- Título: {tsr_data['titulo']}
- Autor primario: {tsr_data['autor_primario']}
- Obra primaria: {tsr_data['obra_primaria']} ({tsr_data['año']})
- Concepto central: {tsr_data['concepto_central']}
- Keywords: {', '.join(tsr_data['keywords'])}
- Autores secundarios: {', '.join(tsr_data['autores_secundarios'])}
- Conexión Reflejos Híbridos: {tsr_data['conexion_RH']}
- Glitch conceptual: {tsr_data['glitch_conceptual']}

DISTRIBUCIÓN REQUERIDA (12-14 fuentes):
**BLOQUE 1: Teoría Clásica (5-6 fuentes)**
- Texto original del autor primario (PDF si existe)
- 2-3 comentaristas canónicos del autor primario
- 1-2 fuentes de autores secundarios mencionados

**BLOQUE 2: Teoría Crítica Relacionada (3-4 fuentes)**
- Textos que conecten el concepto central con otros marcos teóricos
- Diálogos conceptuales (ej: Foucault + Deleuze, Barthes + Eco)
- Críticas o ampliaciones del concepto original

**BLOQUE 3: Investigación Contemporánea (4 fuentes)**
- Papers 2020-2026 sobre: {tsr_data['conexion_RH']}
- Investigación sobre IA, algoritmos, cultura digital, NFT, deepfakes
- Conexiones explícitas entre teoría clásica y tecnología actual

FORMATO JSON (responde SOLO con este JSON):
{{
  "tsr": "{tsr_data['numero']}",
  "titulo": "{tsr_data['titulo']}",
  "cluster": "{tsr_data['cluster']}",
  "fecha_generacion": "{datetime.now().strftime('%Y-%m-%d')}",
  "fuentes": [
    {{
      "numero": 1,
      "bloque": "Teoría Clásica",
      "autor": "Apellido, Nombre",
      "titulo": "Título completo",
      "año": 2024,
      "tipo": "libro|paper|pdf|video|tesis",
      "editorial_revista": "Editorial o Revista Académica",
      "url": "URL completa verificada",
      "doi": "DOI si existe",
      "relevancia": "1-2 frases explicando qué aporta específicamente a TSR{tsr_data['numero']}"
    }}
  ],
  "cobertura_conceptual": {{
    "concepto_central": "% de fuentes que abordan concepto",
    "conexion_RH": "% de fuentes que conectan con RH",
    "glitch": "% de fuentes que problematizan glitch"
  }},
  "nota_metodologica": "Breve nota sobre criterios de selección"
}}

RESTRICCIONES:
- NO inventes URLs
- NO incluyas fuentes sin verificar accesibilidad
- Si no encuentras fuentes suficientes en BLOQUE 3, explícitalo en nota_metodologica
"""

    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_BIBLIOGRAFIA},
                {"role": "user", "content": user_prompt}
            ],
            model="sonar-pro",
            temperature=0.3,
            max_tokens=4000
        )
        
        bibliografia_json = json.loads(completion.choices[0].message.content)
        
        bibliografia_json["metadata_generacion"] = {
            "modelo": completion.model,
            "tokens_entrada": completion.usage.prompt_tokens,
            "tokens_salida": completion.usage.completion_tokens,
            "temperatura": 0.3
        }
        
        return bibliografia_json
        
    except Exception as e:
        return {
            "error": str(e),
            "tsr": tsr_data['numero'],
            "titulo": tsr_data['titulo']
        }


# EJECUCIÓN PRINCIPAL
def generar_capa1_completa():
    """Genera bibliografía para 19 TSR organizados en 7 clústeres."""
    
    print("=" * 80)
    print("🔬 INICIANDO: CAPA 1 - BIBLIOGRAFÍA VERIFICADA")
    print("=" * 80)
    print(f"📊 Total TSR: 19 (TSR102-TSR120)")
    print(f"📚 Clústeres: 7")
    print(f"🎯 Objetivo: ~250 fuentes totales")
    print("=" * 80)
    
    resultados_por_cluster = {}
    errores = []
    
    for tsr in TSR_METADATA:
        cluster_key = tsr['cluster']
        
        if cluster_key not in resultados_por_cluster:
            resultados_por_cluster[cluster_key] = []
        
        print(f"\n🔍 TSR{tsr['numero']}: {tsr['titulo']}")
        print(f"   📖 {tsr['autor_primario']} - {tsr['obra_primaria']}")
        
        resultado = generar_bibliografia_tsr(tsr)
        
        if "error" in resultado:
            print(f"   ❌ ERROR: {resultado['error']}")
            errores.append(resultado)
        else:
            num_fuentes = len(resultado.get('fuentes', []))
            print(f"   ✅ {num_fuentes} fuentes")
            resultados_por_cluster[cluster_key].append(resultado)
    
    # Guardar resultados
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    with open(f"TSR_CAPA1_Completa_{timestamp}.json", "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "capa": "CAPA 1: Bibliografía Verificada",
                "fecha_generacion": datetime.now().isoformat(),
                "total_tsr": len(TSR_METADATA),
                "total_clusters": len(resultados_por_cluster),
                "total_fuentes": sum(len(r.get('fuentes', [])) for cluster in resultados_por_cluster.values() for r in cluster)
            },
            "clusters": resultados_por_cluster,
            "errores": errores
        }, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 80)
    print("🎉 CAPA 1 COMPLETADA")
    print(f"📁 Archivo: TSR_CAPA1_Completa_{timestamp}.json")
    print(f"✅ Exitosos: {len(TSR_METADATA) - len(errores)}/{len(TSR_METADATA)}")
    print("=" * 80)
    
    return resultados_por_cluster


# EJECUTAR
if __name__ == "__main__":
    resultados = generar_capa1_completa()
