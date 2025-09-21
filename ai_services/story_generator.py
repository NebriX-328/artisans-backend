"""
story_generator.py
Generates artisan stories and cultural histories using the Gemini model.
"""

from ai_services.utils.gemini_client import get_gemini_model

def generate_story(artisan_data: dict) -> str:
    """
    Generates a story for an artisan using the centralized Gemini model.

    Args:
        artisan_data (dict): Artisan details including name, craft, location, materials, story points.

    Returns:
        str: Generated artisan story or error message.
    """
    model = get_gemini_model()
    if not model:
        return "Error: Could not initialize Gemini model."

    materials_str = ", ".join(artisan_data.get("materials", []))
    story_points_str = "\n- ".join(artisan_data.get("story_points", []))

    prompt = f"""
    You are a gifted storyteller for an online marketplace that promotes and preserves traditional Indian crafts. 
    Your goal is to connect consumers with the rich heritage behind each artisan's work.

    Artisan Name: {artisan_data.get("name")}
    Craft: {artisan_data.get("craft")}
    Location: {artisan_data.get("location")}
    Materials Used: {materials_str}
    Key Story Points to include:
    - {story_points_str}

    Write a 2–3 paragraph description. The tone should be authentic, warm, and respectful.
    Highlight the craftsmanship, the cultural significance, and the personal story of the artisan.
    """

    try:
        response = model.generate_content(prompt)
        return getattr(response, "text", "Error: No response text returned.")
    except Exception as e:
        return f"Error generating story: {str(e)}"
