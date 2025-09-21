import uuid
import json
from datetime import datetime, timezone
import numpy as np # Import numpy for the test block


def generate_dca(artist_name, craft_name, product_id, creation_date, materials, artist_image_embedding):
    """
    Generates a Digital Certificate of Authenticity as a JSON object,
    including the artist's image embedding.
    """
    # Ensure embedding is a plain Python list (safe for JSON serialization)
    if isinstance(artist_image_embedding, np.ndarray):
        artist_image_embedding = artist_image_embedding.tolist()
    elif not isinstance(artist_image_embedding, list):
        raise TypeError("artist_image_embedding must be a numpy array or list")

    certificate = {
        "certificate_id": f"dca_{uuid.uuid4()}",
        "version": "1.1",
        "issuance_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "artisan_details": {
            "name": artist_name
        },
        "artwork_details": {
            "product_id": product_id,
            "craft_name": craft_name,
            "creation_date": creation_date,
            "materials": materials
        },
        "authenticity_details": {
            "verification_status": "AWAITING_CONSUMER_SCAN",
            "artist_image_embedding": artist_image_embedding
        }
    }
    
    return certificate

# --- This will run when you execute the file for testing ---
if __name__ == "__main__":
    print("--- Generating a sample Digital Certificate of Authenticity ---")

    # For testing, we need to create a fake embedding since we don't have an image here.
    # The size 1280 matches the output of the MobileNetV2 model.
    dummy_embedding = np.random.rand(1280)

    # Sample data for the test, now including the dummy embedding
    sample_dca = generate_dca(
        artist_name="Ramesh Kumar",
        craft_name="Jaipur Blue Pottery",
        product_id="prod_001",
        creation_date="2025-08-15",
        materials=["Quartz powder", "Glass"],
        artist_image_embedding=dummy_embedding
    )

    print(sample_dca)
