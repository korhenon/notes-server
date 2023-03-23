from typing import Annotated

from fastapi import APIRouter, Header

from controller.notes import NotesController
from models.note_request import NotesCreateAndEditRequest

router = APIRouter(prefix="/notes")


@router.get("/all")
def get_all(authorization: Annotated[str, Header()]):
    return NotesController.get_all(authorization)


@router.get("/{note_id}")
def get_by_id(authorization: Annotated[str, Header()], note_id: int):
    return NotesController.get_by_id(authorization, note_id)


@router.post("/create")
def create(body: NotesCreateAndEditRequest, authorization: Annotated[str, Header()]):
    return NotesController.create(body, authorization)


@router.put("/{note_id}")
def update(body: NotesCreateAndEditRequest, authorization: Annotated[str, Header()], note_id: int):
    return NotesController.update(body, authorization, note_id)


@router.delete("/{note_id}")
def delete(authorization: Annotated[str, Header()], note_id: int):
    return NotesController.delete(authorization, note_id)
