from fastapi import File, UploadFile
from pydantic import BaseModel


class ReportInput(BaseModel):
    userId: str
    fileInput: UploadFile = File(...)  # Single file upload