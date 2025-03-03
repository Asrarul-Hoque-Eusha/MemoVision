from fastapi import APIRouter
from models import APIVariables, PathVariables
import os

router = APIRouter()

@router.get("/gallery")
async def show_images_in_gallery():
    try:
        host = PathVariables.host
        retrieved_static_path = PathVariables.retrieved_static_path
        images_list = []
        uploaded_image_paths = os.path.join(PathVariables.directory, PathVariables.retrieved_path)
        for filename in os.listdir(uploaded_image_paths):
            file_type = filename.lower().split(".")[-1]
            if file_type in APIVariables.file_type_list:
                image_path = retrieved_static_path + filename
                images_list.append(image_path)
        return {APIVariables.images: images_list}
    except Exception as error:
        print(APIVariables.error_message,APIVariables.gallery_error,error)
