from pathlib import Path
from fastapi import UploadFile
import shutil
import uuid

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def save_file(file: UploadFile):
    extension = Path(file.filename).suffix
    stored_filename = f"{uuid.uuid4()}{extension}"

    destination = UPLOAD_DIR / stored_filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return stored_filename, str(destination)

def delete_file(stored_filename: str):
    file_path = UPLOAD_DIR/ stored_filename

    if file_path.exists():
        file_path.unlink()