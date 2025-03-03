import base64
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os
import json
import re
from groq import Groq
from enum import Enum
from dataclasses import dataclass

import constants

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

@dataclass
class LlamaConfig:
    model_name: str
    message_format: list
    temperature: float
    max_token: int
    top_k: int

class DictionaryKeys(str, Enum):
    tags = "tags"
    find_tags = "sgat"
    description = "description"
    extract_description_error = "Error in extract_description: "

class LlamaArguments(str, Enum):
    content = "content"
    role = "role"
    user = "user"
    type = "type"
    text = "text"
    image_url = "image_url"
    url = "url"
    image_type = "data:image/jpeg;base64,"
    model_name = "llama-3.2-90b-vision-preview"

def encode_resized_image_to_base64(image_path, size=(150, 150)):
    with Image.open(image_path) as img:
        #convert to RGB if Not img.mode = "RGB"
        if img.mode != "RGB":
            img = img.convert("RGB")
        img = img.resize(size)
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

def get_llama_parameters_config(message_format):
    temperature = 0.4
    max_token = 512
    top_k = 1
    config = LlamaConfig(
        model_name = LlamaArguments.model_name,
        temperature = temperature,
        max_token = max_token,
        top_k = top_k,
        message_format = message_format
    )
    return config

def get_tags_extracted(description):
    search_string = description.lower()[::-1]
    find_tags = DictionaryKeys.find_tags
    length = search_string.find(find_tags)
    tags = description[len(description) - length:]
    description = description[:len(description) - length - 4]
    return tags, description

def extract_description(description):
    if description is None:
        return {DictionaryKeys.description: "", DictionaryKeys.tags: ""}
    cleaned_description = re.sub(r'```python|\n|```|\*\*|\*\*Output:\*\*', '', description)
    if not cleaned_description:
        return {DictionaryKeys.description: "", DictionaryKeys.tags: ""}
    try:
        parsed_text = json.loads(cleaned_description)
        if isinstance(parsed_text, dict) and DictionaryKeys.description in parsed_text and DictionaryKeys.tags in parsed_text:
            if isinstance(parsed_text['tags'], list):
                parsed_text['tags'] = ' '.join(parsed_text['tags'])
            return {DictionaryKeys.description: parsed_text['description'], DictionaryKeys.tags: parsed_text['tags']}
    except json.JSONDecodeError as error:
        cleaned_description = re.sub(r'[^a-zA-Z0-9\s,.\']', '', cleaned_description).strip()
        tags, description = get_tags_extracted(cleaned_description)
        return {DictionaryKeys.description: description,
                DictionaryKeys.tags: tags}

def generate_description(image_url, prompt, storing = False):

    image_base64 = encode_resized_image_to_base64(image_url)
    message_format = [{LlamaArguments.role: LlamaArguments.user, LlamaArguments.content: [
                    {LlamaArguments.type: LlamaArguments.text, LlamaArguments.text: prompt},
                    {
                        LlamaArguments.type: LlamaArguments.image_url,
                        LlamaArguments.image_url: {
                            LlamaArguments.url: LlamaArguments.image_type + image_base64,
                        },
                    },
                ],}]
    llama_config = get_llama_parameters_config(message_format)
    completion = get_llama_answer(llama_config)

    text = completion.choices[0].message.content
    if storing:
        text = extract_description(text)
    return text

def get_message_format(final_prompt):
    message_format = [{LlamaArguments.role: LlamaArguments.user, LlamaArguments.content: [
            {LlamaArguments.type: LlamaArguments.text, LlamaArguments.text: final_prompt},
        ], }]
    return message_format

def get_llama_answer(config: LlamaConfig):
    llama_answer = client.chat.completions.create(
        model=config.model_name,
        messages=config.message_format,
        temperature=config.temperature,
        max_completion_tokens=config.max_token,
        top_p=config.top_k,
        stream=False,
        stop=None,
    )
    return llama_answer

def get_alternate_answer(distance, is_image):
    text_similar_threshold = 0.726
    text_not_matched_threshold = 0.801
    image_similar_threshold = 0.178
    image_not_matched_threshold = .446

    if is_image:
        if distance > image_not_matched_threshold:
            alternate_answer = constants.answer_for_not_matching
        elif distance > image_similar_threshold:
            alternate_answer = constants.answer_for_similar_images
        else:
            alternate_answer = constants.answer_for_matching
    else:
        if distance >= text_not_matched_threshold:
            alternate_answer = constants.answer_for_not_matching
        elif distance > text_similar_threshold:
            alternate_answer = constants.answer_for_similar_images
        else:
            alternate_answer = constants.answer_for_matching
    return alternate_answer

def summarize_description(description, query, first_sample_distance, is_image):
    alternate_answer = get_alternate_answer(first_sample_distance, is_image)
    prompt = constants.description_summarization_prompt.format(description=description, query=query, alternate_answer=alternate_answer)
    message_format = get_message_format(prompt)
    llama_config = get_llama_parameters_config(message_format)
    completion = get_llama_answer(llama_config)
    return completion.choices[0].message.content

def extract_keywords_from_text_query(prompt):
    message_format = get_message_format(prompt)
    llama_config = get_llama_parameters_config(message_format)
    completion = get_llama_answer(llama_config)
    return completion.choices[0].message.content
