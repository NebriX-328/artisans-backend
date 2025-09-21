import os
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env
load_dotenv()
AI_API_KEY = os.getenv("AI_API_KEY")

if not AI_API_KEY:
    raise ValueError("AI_API_KEY not found in .env")

genai.configure(api_key=AI_API_KEY)

# Sample products
PRODUCTS = [
    {"id": "prod_001", "description": "A vibrant, hand-painted Jaipur Blue Pottery vase, featuring traditional Persian floral motifs."},
    {"id": "prod_002", "description": "An elegant, hand-woven Pashmina shawl from Kashmir with intricate sozni embroidery."},
    {"id": "prod_003", "description": "A set of four rustic, hand-carved wooden coasters from Saharanpur, made from sustainable mango wood."},
    {"id": "prod_004", "description": "A delicate Dhokra brass statue of an elephant, crafted by tribal artisans from Bastar."}
]

# Generate product embeddings
def get_product_embeddings():
    product_descriptions = [p["description"] for p in PRODUCTS]
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=product_descriptions,
        task_type="RETRIEVAL_DOCUMENT"
    )
    for i, product in enumerate(PRODUCTS):
        product["embedding"] = np.array(result['embedding'][i], dtype=np.float32)
    return PRODUCTS

# Find best matches
def find_best_matches(user_query, products, top_n=3):
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=user_query,
        task_type="RETRIEVAL_QUERY"
    )
    query_embedding = result['embedding']

    for product in products:
        similarity = np.dot(query_embedding, product["embedding"])
        product["similarity_score"] = similarity

    sorted_products = sorted(products, key=lambda x: x["similarity_score"], reverse=True)
    return sorted_products[:top_n]

# --- Run test ---
if __name__ == "__main__":
    print("Generating product embeddings...")
    products_with_embeddings = get_product_embeddings()
    print("Embeddings generated successfully!\n")

    user_query = "Looking for a traditional housewarming gift"
    print(f"Finding matches for query: '{user_query}'\n")
    best_matches = find_best_matches(user_query, products_with_embeddings)

    for match in best_matches:
        print(f"- {match['id']} | Score: {match['similarity_score']:.4f}")
        print(f"  Description: {match['description']}\n")
