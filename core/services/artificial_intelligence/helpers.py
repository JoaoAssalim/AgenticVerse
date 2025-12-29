import os
import shutil

from fastapi import HTTPException

from core.services.artificial_intelligence import FileLoader

def validate_file(file_path, file_size):
    if file_size > 30 * 10000000:
        raise HTTPException(status_code=400, detail="File size is bigger than 30MB")

    file_loader = FileLoader(file_path)

    if not file_loader._get_loader():
        raise HTTPException(status_code=400, detail="Invalid file type")
        

def save_file_locally(file):
    MEDIA_PATH = "media/"

    if not os.path.exists(MEDIA_PATH):
        os.mkdir(MEDIA_PATH)

    local_file_path = f"{MEDIA_PATH}{file.filename}"

    with open(local_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return local_file_path