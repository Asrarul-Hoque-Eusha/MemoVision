from fastapi import APIRouter
from urllib.parse import unquote
from services.vectordb import get_image_details
from models import APIVariables

router = APIRouter()

@router.get("/image-viewer/{filepath:path}")
async def show_image_details(filepath: str):
    try:
        decoded_filepath = unquote(filepath)
        filepath = decoded_filepath.split('/')[-1]
        description, tags = get_image_details(filepath)
        return {APIVariables.descriptions: description,
                APIVariables.tags: tags}
    except Exception as error:
        print(APIVariables.error_message, APIVariables.viewer, error)
