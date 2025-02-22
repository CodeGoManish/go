import asyncio
import os
import requests
from random import randint
from time import sleep
from dotenv import get_key
from PIL import Image
def open_images(prompt):
    # Generate the filenames for the images
    folder_path = "Data"  # folder where the images are stored
    prompt = prompt.replace(" ", "_")  # Replace spaces in prompt with underscores
    Files = [f"{prompt}_{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            # Try to open and display the image
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)  # Pause for 1 second before showing the next image
        except IOError:
            print(f"Unable to open {image_path}")

# API details for Hugging Face Stable Diffusion model
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

def ensure_data_folder():
    """Ensure the 'Data' folder exists."""
    if not os.path.exists("Data"):
        os.makedirs("Data")

# Function to open and display images based on a given prompt
def open_images(prompt):
    ensure_data_folder()
    prompt = prompt.replace(" ", "_")  # Replace spaces with underscores
    
    for i in range(1, 5):
        image_path = f"Data/{prompt}_{i}.jpg"
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)  # Pause for 1 second before showing the next image
        except IOError:
            print(f"Unable to open {image_path}")

# Async function to send a request to the Hugging Face API
async def query(payload):
    try:
        response = await asyncio.to_thread(requests.post, API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error generating image: {e}")
        return None

# Async function to generate images based on a given prompt
async def generate_images(prompt: str):
    ensure_data_folder()
    tasks = []
    
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}"
        }
        tasks.append(asyncio.create_task(query(payload)))
    
    image_bytes_list = await asyncio.gather(*tasks)
    
    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:
            file_path = f"Data/{prompt.replace(' ', '_')}_{i+1}.jpg"
            with open(file_path, "wb") as f:
                f.write(image_bytes)
            print(f"Image saved: {file_path}")
        else:
            print(f"Failed to generate image {i+1}")

# Wrapper function to generate images
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

# Read the status and prompt from the data file
try:
    with open("Frontend/Files/ImageGeneration.data", "r") as f:
        data = f.read().strip()
        prompt, status = data.split(",")
    
    if status.strip().lower() == "true":
        print("Generating Images...")
        GenerateImages(prompt)
        print("Images Generated!")
        with open("Frontend/Files/ImageGeneration.data", "w") as f:
            f.write("False, False")
    else:
        sleep(1)

except:
    pass
