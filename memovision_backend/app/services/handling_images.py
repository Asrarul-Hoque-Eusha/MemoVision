import os
from PIL import Image
import time
from enum import Enum

from services.ask_llama import generate_description
from services.vectordb import add_to_db_collection
import constants

class StringVariables(str, Enum):
    folder_path = "./images/uploaded_images/"
    error_message = "Error loading image from add_upload_images_to_db: "

def add_upload_images_to_db(image_paths):
    folder_path = StringVariables.folder_path
    start_time = time.time()
    iteration = 0
    for file_name in image_paths:
        iteration += 1
        current_time = time.time()
        if current_time - start_time < 60 and iteration == 16:
            time.sleep(60 - (current_time - start_time))
            iteration = 0
            start_time = time.time()
        image_path = os.path.join(folder_path, file_name)
        try:
            image = Image.open(image_path)
            image = image.resize((224, 224))
            # Prompt to generate description
            prompt = constants.description_generation_prompt

            # Get text description
            text = generate_description(image_path, prompt, storing = True)
            add_to_db_collection(image, text, file_name)
        except Exception as error:
            print(StringVariables.error_message ,file_name, error)
