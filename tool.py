import os
from elevenlabs.conversational_ai.conversation import ClientTools
from langchain_community.tools import DuckDuckGoSearchRun
import google.generativeai as genai
import requests
from io import BytesIO
from PIL import Image

def search_web(parameters):
    query = parameters.get("query")
    search = DuckDuckGoSearchRun()
    return search.run(query)

def save_to_txt(parameters):
    file_name = parameters.get("file_name")
    data = parameters.get("data")
    with open(f"{file_name}.txt", "w", encoding="utf-8") as f:
        f.write(data)
    return "File saved successfully."

def generate_image(parameters):
    prompt = parameters.get("prompt")
    file_name = parameters.get("file_name", "iron_man_blueprint")
    
    # Create directory for generated images
    dir_name = "generated_images"
    os.makedirs(dir_name, exist_ok=True)
    file_path = os.path.join(dir_name, f"{file_name}.png")
    
    # Initialize Google Gemini API
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # Generate image using Google Imagen (or Gemini image generation model)
    # Using Imagen 3 via google-generativeai SDK
    image_model = genai.GenerativeModel("imagen-3.0-generate-002")
    result = image_model.generate_images(
        prompt=prompt,
        number_of_images=1,
        safety_filter_level="block_medium_and_above",
        person_generation="allow_adult",
    )
    
    for generated_image in result.generated_images:
        image = Image.open(BytesIO(generated_image.image.image_bytes))
        image.save(file_path)
    
    return f"Image successfully generated and saved as {file_path}."

# Register all tools
client_tools = ClientTools()
client_tools.register("search_web", search_web)
client_tools.register("save_to_txt", save_to_txt)
client_tools.register("generate_image", generate_image)
