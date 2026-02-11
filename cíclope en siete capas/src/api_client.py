from perplexity import Perplexity
import os

# Configurar API key (agrega tu key al .env o directamente)
client = Perplexity(api_key="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")  # O usa os.environ.get("PPLX_API_KEY")

# Test básico
search = client.search.create(
    query="latest AI developments 2024",
    max_results=5,
    max_tokens_per_page=2048
)

for result in search.results:
    print(f"{result.title}: {result.url}")
