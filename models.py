from datetime import datetime
from config import db, ma


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
    notes : db.relationship
        The relationship between Person and Note
    '''
    __tablename__ = 'person'
    person_id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32), index=True)
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    notes = db.relationship(
        # 'Note' defines the SQLAlchemy class Person is related to
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
    Defines how the attributes of a class will be converted into JSON-friendly
    formats

    Parent: ma.ModelSchema
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
