import requests
import base64
import json
import re


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_description(description):
    try:
        description = re.sub(r'```python|\n|```', '', description)
        description = json.loads(description)
        if type(description['tags']) == list:
            description['tags'] = ' '.join(description['tags'])
        text = {
            'description': description['description'],
            'tags': description['tags']
        }
        return text
    except Exception as e:
        print(f"Error in extract_description: {e}")

def generate_description(image_url, custom_prompt, storing = False):
    url = "http://localhost:11434/api/generate"
    image = encode_image_to_base64(image_url)
    payload = {
        "model": "llava",
        "prompt": custom_prompt,
        "images": [image]
    }
    response = requests.post(url, json=payload)
    try:
        # Split the response text into separate lines
        response_lines = response.text.strip().split('\n')

        # Extract and concatenate the 'response' part from each line
        full_response = ''.join(
            json.loads(line)['response'] for line in response_lines if 'response' in json.loads(line))
        text = full_response
        print(text)
        if storing:
            text = extract_description(text)
        return text
        #return full_response
    except Exception as e:
        return f"Error: {e}"


prompt = """### Task
                        Analyze the given image and generate a structured description along with relevant tags.
                        Follow the output format strictly:
                        ### Action
                        1. Description:
                           - Provide a concise yet detailed summary of the image in 130 words or fewer.
                           - Capture key elements such as scene (e.g., sunset, sunrise, sunny), landscape (e.g., beach, forest, hill, field), events (e.g., birthday, wedding, tours), objects (e.g., tree, car, bus, tiger, road, building etc.) with quantity, humans (e.g., boy, girl, children, man, women etc.) with quantity, activities (e.g., running, walking, hiking, playing, skating etc.), and pets (e.g., cat, dog, bird etc.) if any.
                           - The description should be informative, engaging, and accurately reflect the image.

                        2. Tags:
                           - Generate a space-separated string of tags summarizing the key elements in the image.
                           - Include tags for the scene (e.g., sunset, sunrise, sunny), landscape (e.g., beach, forest, hill, field), events (e.g., birthday, wedding, tours), objects (e.g., tree, car, bus, tiger, lion, road, building etc.) with quantity, humans (e.g., boy, girl, children, man, women etc.) with quantity, activities (e.g., running, walking, hiking, playing, skating etc.), and pets (e.g., cat, dog, bird etc.) if any.
                           - Avoid redundant or overly generic tags like environment, image, scene, scenery, outdoor, picture, nature, attire. Make sure the tags are specific to the image.
                        ### Guidelines
                        - **Strictly return the output as a python dictionary.**
                        - The **output MUST be a valid Python dictionary with exactly two keys: "description" and "tags"**.
                        - **DO NOT** include any additional text, markdown, or explanation.
                        - The description and tags should only contain relevant details specific to the image.
                        - Follow output structure strictly. Any deviations from this format will result in incorrect output. An example of expected output format is given below:
                            {
                                "description": "A group of four individuals, dressed in red and black attire, are positioned in front of a lush green hill. The scene is set against a backdrop of trees and bushes, with a clear blue sky visible above. The atmosphere suggests a daytime setting, likely during a sunny day.",
                                "tags": "hills forest tour travels enjoy trees bushes sky daytime sunny people red black"
                            }
                        """

#Testing the generate_description function:


folder_path = "D:/30177/30177ConversationalMemoryBot/images/uploaded_images/New_folder/"
images = ["2024-10-02-banner.png","ULVH-cats-playing-shutterstock_1211910061-870x400.jpeg","The-Rooftop-at-Pier-17-concert.webp","tracker.jpg","4a.jpg","68.jpg","beach.jpg","banner6.jpg","cat.jpg","dog.jpg","canal.jpg","Boatincanal.jpg","7.webp"]
for image in images:
    image_path = folder_path + image
    description = generate_description(image_path, prompt, True)
    print(type(description))
    #print(description)
    print(description['description'])
    print(description['tags'])
#description = re.sub(r'```python\n|```', '', description)
#print(description)
#description = json.loads(description)
#description = extract_description(description)
#print(description['description'])
#print(description['tags'])

