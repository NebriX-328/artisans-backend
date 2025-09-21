from ai_services.recommendation.product_recommendation import recommend_products
from ai_services.verification.dca_generator import generate_dca
from ai_services.story_generator import generate_story

def run_ai_services(user_query: str, product_data: dict, artisan_details: dict):
    """
    Runs all AI services and returns combined results.

    Args:
        user_query (str): User input for product recommendation.
        product_data (dict): Data required for DCA generation.
        artisan_details (dict): Data required for generating artisan stories.

    Returns:
        dict: Contains product recommendations, DCA code, and artisan story.
    """
    recommendations = recommend_products(user_query)
    dca_code = generate_dca(product_data)
    story = generate_story(artisan_details)

    return {
        "recommendations": recommendations,
        "dca_code": dca_code,
        "story": story
    }

# Quick test
if __name__ == "__main__":
    sample_query = "Looking for a traditional gift for a friend's new home"
    sample_product_data = {"product_code": "P001", "name": "Blue Pottery Vase", "price": 1200}
    sample_artisan_data = {
        "name": "Ramesh Kumar",
        "craft": "Jaipur Blue Pottery",
        "location": "Jaipur, Rajasthan",
        "materials": ["Quartz powder", "Glass", "Multani Mitti (Fuller's Earth)"],
        "story_points": [
            "Family has been in this craft for 5 generations.",
            "Learned the technique from his grandfather.",
            "Uses a unique turquoise-blue dye made from a secret family recipe.",
            "Each piece is hand-painted with traditional Persian motifs."
        ]
    }

    result = run_ai_services(sample_query, sample_product_data, sample_artisan_data)
    print(result)
