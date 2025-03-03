from fastapi import APIRouter, UploadFile
import os

from services.handling_images import add_upload_images_to_db
from models import APIVariables, PathVariables, IncludeEnum
from services.vectordb import get_image_details



router = APIRouter()

@router.post("/batch-upload/")
async def upload_images(files: list[UploadFile]):
    try:
        upload_folder_path = PathVariables.upload_folder_path.value
        os.makedirs(upload_folder_path, exist_ok=True)
        added_file_paths = []
        exists_file_paths = []
        for image in files:
            file_name = image.filename
            file_extension = file_name.split(".")[-1]
            if file_extension in APIVariables.file_type_list:
                ids,_ = get_image_details(file_name)
                if ids == IncludeEnum.empty_id:
                    file_path = f'{upload_folder_path}/{file_name}'
                    with open(file_path, 'wb+') as fl:
                        fl.write(image.file.read())
                    added_file_paths.append(file_name)
                else:
                    exists_file_paths.append(file_name)
        add_upload_images_to_db(added_file_paths)

        return {
            APIVariables.upload_message: APIVariables.upload_success,
            APIVariables.file_exists: exists_file_paths
        }
    except Exception as error:
        return {
            APIVariables.upload_message: APIVariables.upload_error,
            APIVariables.file_exists: []
        }