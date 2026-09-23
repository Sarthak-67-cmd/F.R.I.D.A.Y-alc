import os
from elevenlabs.conversational_ai.conversation import ClientTools
from langchain_community.tools import DuckDuckGoSearchRun
from openai import OpenAI
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
    
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Generate image using DALL-E 3
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    
    image_url = response.data[0].url
    
    # Download and save the image locally
    img_response = requests.get(image_url)
    img = Image.open(BytesIO(img_response.content))
    img.save(file_path)
    
    return f"Image successfully generated and saved as {file_path}."

# Register all tools
client_tools = ClientTools()
client_tools.register("search_web", search_web)
client_tools.register("save_to_txt", save_to_txt)
client_tools.register("generate_image", generate_image)
