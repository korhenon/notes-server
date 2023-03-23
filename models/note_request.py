from pydantic import BaseModel


class NotesCreateAndEditRequest(BaseModel):
    title: str
    text: str
