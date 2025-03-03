import os
from enum import Enum

class DeleteImage(str, Enum):
    folder_path = "./images/new_folder/"
    success_message = "All images deleted successfully!"

def delete_query_image():
    folder_path = DeleteImage.folder_path

    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp")):
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)
    print(DeleteImage.success_message)
