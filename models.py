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
    timestamp: datetime
        The UTC timestamp of when a person was added/updated to the table
    '''
    __tablename__ = 'person'
    person_id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32), index=True)
    fname = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow,
                          onupdate=datetime.utcnow)


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
