# This module handles the Note API definitions. It's similar to people.py
# except it must handle both person_id and note_id as defined in swagger.yml

from config import db
from flask import make_response, abort
from models import Person, Note, NoteSchema


def read_all():
    '''
    This function responds to a request for /api/people/notes with the complete
    list of notes, sorted by note timestamp

    Returns
    -------
    data : list
        A JSON list of all notes for all people
    '''
    # Query the database for all the notes
    notes = Note.query.order_by(db.desc(Note.timestamp)).all()

    # Serialize the list of notes from our data
    note_schema = NoteSchema(many=True, exclude=['person.notes'])
    data = note_schema.dump(notes).data

    return data
