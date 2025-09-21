from decouple import config
import numpy as np
import google.generativeai as genai
from products.models import Product

# Load GEMINI API key
AI_API_KEY = config('AI_API_KEY')
if not AI_API_KEY:
    raise ValueError("AI_API_KEY not found in .env")

genai.configure(api_key=AI_API_KEY)


def get_product_embeddings():
    """Fetch products from DB and generate embeddings."""
    products = Product.objects.all()
    descriptions = [
        f"{p.name}. {p.craft_type}. Artisan: {p.artisan_name}" for p in products
    ]
    if not descriptions:
        return []

    result = genai.embed_content(
        model="models/text-embedding-004",
        content=descriptions,
        task_type="RETRIEVAL_DOCUMENT"
    )

    for i, product in enumerate(products):
        product.embedding_array = np.array(result['embedding'][i], dtype=np.float32)

    return products


def find_best_matches(user_query, products_with_embeddings, top_n=3):
    """Find top-N matching products for a query."""
    if not products_with_embeddings:
        return []

    result = genai.embed_content(
        model="models/text-embedding-004",
        content=user_query,
        task_type="RETRIEVAL_QUERY"
    )
    query_embedding = result['embedding']

    matches = []
    for product in products_with_embeddings:
        product_embedding = getattr(product, "embedding_array", None)
        if product_embedding is not None:
            similarity = np.dot(query_embedding, product_embedding)
            matches.append((similarity, product))

    matches.sort(key=lambda x: x[0], reverse=True)
    top_matches = [p[1] for p in matches[:top_n]]

    return [
        {
            "id": p.id,
            "product_code": p.product_code,
            "name": p.name,
            "price": str(p.price),
            "artisan_name": p.artisan_name,
            "craft_type": p.craft_type,
        }
        for p in top_matches
    ]


def recommend_products(user_query, top_n=3):
    """Main function to recommend products for a query."""
    products = get_product_embeddings()
    return find_best_matches(user_query, products, top_n)


def run_ai_services(prompt):
    """Example AI call for text generation."""
    response = genai.text.generate(model="text-bison-001", prompt=prompt)
    return response.text
