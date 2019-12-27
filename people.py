# This connects to the swagger.yml file:
# We configured Connexion with the operationId value to call the people module
# and the read function within the module when the API gets an HTTP GET
# This means this file must exist and contain a read() function

# Project modules
from config import db
from models import Note, Person, PersonSchema

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort


def get_timestamp():
    '''
    Generates a string representation of the current timestamp

    Returns
    -------
    str
        String representation of the current timestamp
    '''
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Preliminary Data to serve with our API
# PEOPLE = {
#     "Farrell": {
#         "fname": "Doug",
#         "lname": "Farrell",
#         "timestamp": get_timestamp()
#     },
#     "Brockman": {
#         "fname": "Kent",
#         "lname": "Brockman",
#         "timestamp": get_timestamp()
#     },
#     "Easter": {
#         "fname": "Bunny",
#         "lname": "Easter",
#         "timestamp": get_timestamp()
#     },
# }


# Create a handler for our read (GET) people
def read_all():
    '''
    This function responds to a request for /api/people with the complete
    lists of people

    Returns
    -------
    str
        A JSON string of list of people ordered by last name
    '''
    # Create list of people from our data
    people = Person.query.order_by(Person.lname).all()

    # Serialize the data for the response
    # many = True tells PersonSchema to expect an iterable to serialize
    person_schema = PersonSchema(many=True)

    # Return an object having a data attribute that Connexion can convert to
    # JSON
    data = person_schema.dump(people)
    return data


# Create handler for our read where an lname parameter is provided
def read_one(person_id):
    '''
    This function responds to a request for /api/people/{person_id} with one
    matching person from people

    Parameters
    ----------
    person_id: int
        ID of person to find

    Returns
    -------
    Person
        Person matching ID
    '''
    # Get the person requested
    # The .outerjoin (left outer join in SQL) is necessary for the case where
    # a user of the application has created a new Person, which has no notes
    # related to it. Outer join ensures the SQL query returns a Person, even
    # if there are no note rows to join with
    # A join is like an AND operation and returns nothing if a Person exists
    # but has no Notes
    # An outer join is an OR operation which returns a Person even if it has
    # no Notes
    person = (
        Person.query.filter(Person.person_id == person_id)
        .outerjoin(Note)
        .one_or_none()
    )

    # Did we find a person?
    if person is not None:
        # Serialize the data for the response
        person_schema = PersonSchema()
        data = person_schema.dump(person)

        return data
    # Otherwise, nope, not found
    else:
        abort(404, f'Person with Id: {person_id} not found')


def create(person):
    '''
    This function creates a new person in the people structure based on the
    passed in person data

    Parameters
    ----------
    person: Person
        Person to create in people structure

    Returns
    -------
    201
        On success
    409
        On person exists
    '''
    fname = person.get("fname")
    lname = person.get("lname")

    existing_person = (
        Person.query.filter(Person.fname == fname)
        .filter(Person.lname == lname)
        .one_or_none()
    )

    # Can we insert this person?
    if existing_person is None:
        # Create a person instance using the schema and the passed-in person
        schema = PersonSchema()
        new_person = schema.load(person, session=db.session).data

        # Add the person to the database
        db.session.add(new_person)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_person)
        return data, 201
    # Otherwise, they exist, that's an error
    else:
        abort(409, f'Person {fname} {lname} already exists!')


def update(person_id, person):
    '''
    This function updates an existing person in the people structure

    Parameters
    ----------
    person_id: int
        Id of the person to update in the people structure
    person: Person
        Person to update

    Returns
    -------
    Person
        Updated person structure
    '''
    # Get the person requested from the db into session
    update_person = Person.query.filter(
        Person.person_id == person_id
    ).one_or_none()

    # Did we find an existing person?
    if update_person is not None:
        # Turn the passed in person into a db object
        schema = PersonSchema()
        update = schema.load(person, session=db.session).data

        # Set the id to the person we want to update
        update.person_id = update_person.person_id

        # Merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # Return the updated person in the response
        data = schema.dump(update_person)

        return data, 200
    # Otherwise, nope, that's an error
    else:
        abort(404, f'Person with Id {person_id} not found')


def delete(person_id):
    '''
    This function deletes a person from the people structure

    Parameters
    ----------
    person_id: int
        Id of the person to delete

    Returns
    -------
    200
        On successful delete
    404
        If not found
    '''
    # Get the person requested
    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    # Did we find a person?
    if person is not None:
        db.session.delete(person)
        db.session.commit()

        return make_response(f'Person {person_id} successfully deleted', 200)
    # Otherwise, nope, person to delete not found
    else:
        abort(404, f'Person with Id {person_id} not found')
