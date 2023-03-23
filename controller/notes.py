import datetime

from controller.auth import AuthController
from database.models import Note
from models.notes_response import NoteResponse, NotesGetAllResponse, NotesGetResponse, NotesCreateAndEditResponse
from models.note_request import NotesCreateAndEditRequest


def convert_to_note_response(note: Note) -> NoteResponse:
    return NoteResponse(
        id=note.id,
        author_id=note.author.id,
        title=note.title,
        text=note.text,
        edit_datetime=str(note.edit_datetime)
    )


class NotesController:
    @staticmethod
    def get_all(token: str) -> NotesGetAllResponse:
        if AuthController.can_authenticate(token):
            user = AuthController.authenticate(token)
            notes = Note.select().where(Note.author_id == user.id)
            response = []
            for note in notes:
                response.append(convert_to_note_response(note))
            return NotesGetAllResponse(notes=response)
        return NotesGetAllResponse(notes=[], message="User doesn't authenticated!")

    @staticmethod
    def get_by_id(token: str, note_id: int) -> NotesGetResponse:
        if AuthController.can_authenticate(token):
            user = AuthController.authenticate(token)
            notes = Note.select().where(Note.id == note_id)
            if len(notes) == 0:
                return NotesGetResponse(message="Note doesn't exists!")
            if notes[0].author.id != user.id:
                return NotesGetResponse(message="Note doesn't yours!")
            return NotesGetResponse(
                note=convert_to_note_response(notes[0]),
            )
        return NotesGetResponse(message="User doesn't authenticated!")

    @staticmethod
    def create(body: NotesCreateAndEditRequest, token: str) -> NotesCreateAndEditResponse:
        if AuthController.can_authenticate(token):
            user = AuthController.authenticate(token)
            note = Note()
            note.title = body.title
            note.text = body.text
            note.author = user
            note.save()
            return NotesCreateAndEditResponse(successful=True)
        return NotesCreateAndEditResponse(successful=False, message="User doesn't authenticated!")

    @staticmethod
    def update(body: NotesCreateAndEditRequest, token: str, note_id: int) -> NotesCreateAndEditResponse:
        if AuthController.can_authenticate(token):
            user = AuthController.authenticate(token)
            notes = Note.select().where(Note.id == note_id)
            if len(notes) == 0:
                return NotesCreateAndEditResponse(message="Note doesn't exists!", successful=False)
            if notes[0].author.id != user.id:
                return NotesCreateAndEditResponse(message="Note doesn't yours!", successful=False)
            note = notes[0]
            note.title = body.title
            note.text = body.text
            note.edit_datetime = datetime.datetime.now()
            note.save()
            return NotesCreateAndEditResponse(successful=True)
        return NotesCreateAndEditResponse(message="User doesn't authenticated!", successful=False)

    @staticmethod
    def delete(token, note_id) -> NotesCreateAndEditResponse:
        if AuthController.can_authenticate(token):
            user = AuthController.authenticate(token)
            notes = Note.select().where(Note.id == note_id)
            if len(notes) == 0:
                return NotesCreateAndEditResponse(message="Note doesn't exists!", successful=False)
            if notes[0].author.id != user.id:
                return NotesCreateAndEditResponse(message="Note doesn't yours!", successful=False)
            note = notes[0]
            note.delete_instance()
            return NotesCreateAndEditResponse(successful=True)
        return NotesCreateAndEditResponse(message="User doesn't authenticated!", successful=False)
