from typing import Optional

from pydantic import BaseModel


class NoteResponse(BaseModel):
    id: int
    author_id: int
    title: str
    text: str
    edit_datetime: str


class NotesCreateAndEditResponse(BaseModel):
    successful: bool
    message: Optional[str]


class NotesGetAllResponse(BaseModel):
    notes: list[NoteResponse]
    message: Optional[str]


class NotesGetResponse(BaseModel):
    note: Optional[NoteResponse]
    message: Optional[str]
