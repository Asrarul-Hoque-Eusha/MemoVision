from enum import Enum

class IncludeEnum(str, Enum):
    ids = "ids"
    documents = "documents"
    metadata = "metadatas"
    distances = "distances"
    collection_name = "image_text_collection"
    directory = "./images/new_folder/"
    empty_string = ""
    empty_id = "None"

class APIVariables(str, Enum):
    user_query = "query"
    user_query_image = "query_image"
    retrieved_image = "retrieved_image"
    answer = "answer"
    images = "images"
    descriptions = "descriptions"
    tags = "tags"
    chatbot_error = " ask_query: "
    error_message = "Error in "
    gallery_error = " show_images_in_gallery "
    uploader_error = " upload_images "
    viewer_error = " show_image_details: "
    file_type_list = ["png", "jpg", "jpeg", "webp"]
    fastapi_running_message = "FastAPI is running"
    message = "message"
    upload_message = "upload_message"
    upload_success = "Files uploaded successfully."
    upload_error = "Files upload failed."
    file_added = "file_added"
    file_exists = "file_exists"
    ask_llm = "ask_llm"
    ask_database = "ask_database"
    describe_image = "describe_image"

class PathVariables(str, Enum):
    host = "http://localhost:8000"
    retrieved_path = "uploaded_images/"
    upload_folder_path = './images/uploaded_images/'
    retrieved_static_path = f"{host}/static/{retrieved_path}"
    query_img_path = "new_folder/"
    query_static_path = f"{host}/static/{query_img_path}"
    directory = "./images"