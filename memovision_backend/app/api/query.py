from fastapi import APIRouter, Form, File, UploadFile
import time

from services.vectordb import query_database
from services.ask_llama import generate_description, summarize_description
from models import APIVariables, PathVariables
from services.ques_category import find_query_type
import constants
router = APIRouter()

@router.post("/ask-query/")
async def ask_query(
        query: str | None = Form(None),
        image: UploadFile | None = File(None)
    ):
    retrieved_static_path = PathVariables.retrieved_static_path
    query_image = None
    image_name = None
    images_list = None
    if image:
        query_img_path = PathVariables.query_img_path
        query_static_path = PathVariables.query_static_path
        upload_time = str(time.time())
        query_image = f"{query_static_path}{upload_time}{image.filename}"
        #
        image_name = PathVariables.directory + '/' + query_img_path + upload_time + image.filename
        with open(image_name, 'wb+') as fl:
            fl.write(image.file.read())
    try:
        invoke_function = APIVariables.ask_database
        if query:
            invoke_function = find_query_type(query)
        if invoke_function == APIVariables.ask_llm:
            descriptions = constants.ask_llm_answer
        elif invoke_function == APIVariables.describe_image and image:
            prompt = constants.image_describer_prompt.format(query=query)
            descriptions = generate_description(image_name,prompt)
        else:
            is_image = False
            if image:
                image_name = image_name.split('/')[-1]
                is_image = True
            instruction, answer = query_database(query, image_name)
            images_list = answer["ids"][0]
            descriptions = answer["documents"][0]
            if len(descriptions) == 0:
                descriptions = constants.no_image_found_message
            else:
                first_distance = answer['distances'][0][0]
                descriptions = summarize_description(descriptions, instruction, first_distance, is_image)
            images_list = [retrieved_static_path + image for image in images_list]
        return {
            APIVariables.user_query: query,
            APIVariables.user_query_image: query_image,
            APIVariables.retrieved_image: images_list,
            APIVariables.answer: descriptions
        }
    except Exception as error:
        descriptions = constants.chatbot_error_description
        return {
            APIVariables.user_query: query,
            APIVariables.user_query_image: query_image,
            APIVariables.retrieved_image: images_list,
            APIVariables.answer: descriptions
        }