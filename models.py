from datetime import datetime
from config import db, ma
from marshmallow import fields

# NOTE: Marshmallow is the module that translates SQLAlchemy objects into
#       Python objects suitable for creating JSON strings


class Person(db.Model):
    '''
    Class used to represent a Person

    Parent: db.Model

    Attributes
    ----------
    __tablename__ : str
        A string that states the name of the table
    person_id : int
        The unique id of a person in the person table
    lname : str
        The last name of the person
    fname : str
        The first name of the person
    timestamp : datetime
        The UTC timestamp of when a person was added/updated to the table
    notes : list
        List of notes created by a Person
    '''
    __tablename__ = 'person'
    person_id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32))
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    # Set up the relationship between Person and Note
    notes = db.relationship(
        # 'Note' defines what the SQLAlchemy class Person is related to
        # We use string as a forward reference which handles problems caused
        # by something that is needed but isn't defined until later in the code
        'Note',
        # backref='person' creates a back reference to person
        # Each instance of Note will contain a person attribute which
        # references the parent object (Person)
        # Having a reference to the parent in the child can be useful if your
        # code iterates over notes and has to include info about the parent
        # (this happens frequently in display rendering code)
        backref='person',
        # cascade determines how to treat Note instances when changes are made
        # to the Person instance
        # e.g. When a Person is deleted, this parameter tells SQLAlchemy to
        #      delete all Note instances associated with it
        cascade='all, delete, delete-orphan',
        # single_parent=True is required if delete-orphan is part of the
        # cascade parameter
        # This tells SQLAlchemy not to allow oprhaned Note instances to exist
        # because each Note has a single parent
        single_parent=True,
        # ordery_by tells SQLAlchemy how to sort the Note instances associated
        # with a Person. By default the notes attribute list will contain Note
        # objects in an unknown order. desc() sorts notes in descending order
        # (ascending is the default)
        order_by='desc(Note.timestamp)'
    )


class Note(db.Model):
    '''
    Class used to represent a Note

    Parent: db.Model

    Attributes
    ----------
    __tablename__ : str
        A string that states the name of the table
    note_id : int
        The unique id of a note in the note table
    person_id : int
        A number corresponding to the owner of the note
    content : str
        The actual text of the note
    timestamp : datetime
        The UTC timestamp of when a note was added/updated to the table
    '''
    __tablename__ = 'note'
    note_id = db.Column(db.Integer, primary_key=True)
    # Relate the Note class to the Person class using person.person_id
    # This and Person.notes are how SQLAlchemy knows what to do when
    # interacting with Person and Note objects
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    # nullable=False indicates it's ok to create a new empty note
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class PersonSchema(ma.ModelSchema):
    '''
    Defines how the attributes of Person will be converted into JSON-friendly
    formats

    Parent: ma.ModelSchema

    Attributes
    ----------
    notes : list
        List of notes related to a Person, default is empty list
    '''
    class Meta:
        '''
        Required by ModelSchema. Used to find the SQLAlchemy model Person and
        the db.session in order to extract Person attributes and their types in
        order to serialize/deserialize them.

        Attributes
        ----------
        model : Person
            The SQLAlchemy model to use to serialize/deserialize data
        sqla_session: db.session
            The database session to use to introspect and determine attribute
            data types
        '''
        model = Person
        sqla_session = db.session

    # RECALL: many = True indicates a one-to-many relationship, so Marshmallow
    #         will serialize all related notes
    notes = fields.Nested('PersonNoteSchema', default=[], many=True)


# The PersonNoteSchema class defines what a Note object looks like as
# Marshmallow serializes the notes list
class PersonNoteSchema(ma.ModelSchema):
    '''
    This class exists to get around a recursion issue

    Parent: ma.ModelSchema

    Attributes
    ----------
    note_id : int
        The unique id of a note in the note table
    person_id : int
        A number corresponding to the owner of the note
    content : str
        The actual text of the note
    timestamp : str
        The string representation of a Person/Note timestamp
    '''
    note_id = fields.Int()
    person_id = fields.Int()
    content = fields.Str()
    timestamp = fields.Str()


class NoteSchema(ma.ModelSchema):
    '''
    Defines how the attributes of Note will be converted into JSON-friendly
    formats

    Parent: ma.ModelSchema

    Attributes
    ----------
    person : Person
        Person related to a Note, default is None
    '''
    class Meta:
        '''
        Required by ModelSchema. Used to find the SQLAlchemy model Note and
        the db.session in order to extract Note attributes and their types in
        order to serialize/deserialize them.

        Attributes
        ----------
        model : Note
            The SQLAlchemy model to use to serialize/deserialize data
        sqla_session: db.session
            The database session to use to introspect and determine attribute
            data types
        '''
        model = Note
        sqla_session = db.session

    # This attribute comes from the db.relationship definition parameter
    # backref='person'. It is nested but because it doesn't have a many=True
    # parameter, there is only a single person connected
    person = fields.Nested('NotePersonSchema', default=None)


class NotePersonSchema(ma.ModelSchema):
    '''
    This class exists to get around a recursion issue

    Parent: ma.ModelSchema

    Attributes
    ----------
    person_id : int
        The unique id of a person in the person table
    lname : str
        Last name corresponding to the owner of the note
    fname : str
        First name corresponding to the owner of the note
    timestamp : str
        The string representation of a Person/Note timestamp
    '''
    person_id = fields.Int()
    lname = fields.Str()
    fname = fields.Str()
    timestamp = fields.Str()
