import os
import sys
import numpy as np
import requests
from io import BytesIO
from keras.utils import load_img, img_to_array
from ai_services.utils.gemini_client import get_gemini_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.models import Model
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np

# Load model once at startup (without the classification head)
embedding_model = ResNet50(weights="imagenet", include_top=False, pooling="avg")


# This block adds the main project folder to Python's path before other imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# All imports should be at the top
from ai_services.utils.gemini_client import get_gemini_model

# --- Load a pre-trained deep learning model ---
base_model = MobileNetV2(weights='imagenet', include_top=True)
model = Model(inputs=base_model.input, outputs=base_model.layers[-2].output)
# ---------------------------------------------


def generate_image_embedding(image_path):
    try:
        if image_path.startswith("http://") or image_path.startswith("https://"):
            response = requests.get(image_path)
            response.raise_for_status()
            img = load_img(BytesIO(response.content), target_size=(224, 224))
        else:
            img = load_img(image_path, target_size=(224, 224))

        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)  # ResNet preprocessing

        return embedding_model.predict(img_array)[0].tolist()
    except Exception as e:
        raise ValueError(f"Error processing image {image_path}: {str(e)}")

def verify_authenticity(embedding1, embedding2, threshold=0.65):
    """
    Compares two image embeddings using cosine similarity.
    """
    if embedding1 is None or embedding2 is None:
        return {"match": False, "reason": "One or both embeddings are invalid."}

    embedding1 = embedding1.reshape(1, -1)
    embedding2 = embedding2.reshape(1, -1)
    
    similarity_score = float(cosine_similarity(embedding1, embedding2)[0][0])
    is_match = similarity_score >= threshold
    
    return {"match": is_match, "similarity_score": float(similarity_score)}

def summarize_verification_result(verification_data):
    """
    Generates a user-friendly summary of the verification result.
    """
    gemini_model = get_gemini_model('gemini-1.5-flash-latest')
    if gemini_model is None:
        return "Could not generate summary."

    if verification_data['match']:
        prompt = f"""
        The product verification was successful with a high similarity score of {verification_data['similarity_score']:.2f}. 
        Write a very short, reassuring, one-sentence summary for the user confirming their product is authentic.
        Example: 'Your product has been successfully verified as authentic!'
        """
    else:
        prompt = f"""
        The product verification failed with a low similarity score of {verification_data['similarity_score']:.2f}.
        Write a very short, polite, one-sentence summary for the user.
        Do not sound alarming. Suggest they contact customer support for next steps.
        Example: 'This product could not be verified, please contact support for assistance.'
        """
    response = gemini_model.generate_content(prompt)
    return response.text.strip()


# --- This will run when you execute the file for testing ---
if __name__ == "__main__":
    artist_image_path = "artist_scan.jpg"
    consumer_match_path = "consumer_scan_match.jpg"
    consumer_mismatch_path = "consumer_scan_mismatch.jpg"
    
    print("--- Simulating Authenticity Verification using Image Embeddings ---")

    print("\n--- Test Case 1: Verifying a MATCHING product ---")
    artist_embedding = generate_image_embedding(artist_image_path)
    consumer_match_embedding = generate_image_embedding(consumer_match_path)
    match_result = verify_authenticity(artist_embedding, consumer_match_embedding)
    print(f"Verification Result: {match_result}")
    if match_result['match'] is not None:
        summary = summarize_verification_result(match_result)
        print(f"AI Summary: {summary}\n")
    
    print("--- Test Case 2: Verifying a MISMATCHING product ---")
    artist_embedding = generate_image_embedding(artist_image_path) # Re-use the artist's scan
    consumer_mismatch_embedding = generate_image_embedding(consumer_mismatch_path)
    mismatch_result = verify_authenticity(artist_embedding, consumer_mismatch_embedding)
    print(f"Verification Result: {mismatch_result}")
    if mismatch_result['match'] is not None:
        summary = summarize_verification_result(mismatch_result)
        print(f"AI Summary: {summary}")
