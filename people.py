# This connects to the swagger.yml file:
# We configured Connexion with the operationId value to call the people module
# and the read function within the module when the API gets an HTTP GET
# This means this file must exist and contain a read() function

# Project modules
from config import db
from models import Person, PersonSchema

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


# Data to serve with our API
PEOPLE = {
    "Farrell": {
        "fname": "Doug",
        "lname": "Farrell",
        "timestamp": get_timestamp()
    },
    "Brockman": {
        "fname": "Kent",
        "lname": "Brockman",
        "timestamp": get_timestamp()
    },
    "Easter": {
        "fname": "Bunny",
        "lname": "Easter",
        "timestamp": get_timestamp()
    },
}


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
    return person_schema.dump(people).data


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
    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    # Did we find a person?
    if person is not None:
        # Serialize the data for the response
        person_schema = PersonSchema()

        return person_schema.dump(person).data
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

    existing_person = Person.query \
        .filter(Person.fname == fname) \
        .filter(Person.lname == lname) \
        .one_or_none()

    # Can we insert this person?
    if existing_person is None:
        # Create a person instance using the schema and the passed-in person
        schema = PersonSchema()
        new_person = schema.load(person, session=db.session).data

        # Add the person to the database
        db.session.add(new_person)
        db.session.commit()

        # Serialize and return the newly created person in the response
        return schema.dump(new_person).data, 201
    # Otherwise, they exist, that's an error
    else:
        abort(409, f'Person {fname} {lname} already exists!')


def update(lname, person):
    '''
    This function updates an existing person in the people structure

    Parameters
    ----------
    lname: str
    person: PERSON

    Returns
    -------
    PEOPLE
        Updated person structure
    '''
    # Does the person exist in people?
    if lname in PEOPLE:
        PEOPLE[lname]["fname"] = person.get("fname")
        PEOPLE[lname]["timestamp"] = get_timestamp()

        return PEOPLE[lname]
    # Otherwise, nope, that's an error
    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )


def delete(lname):
    '''
    This function deletes a person from the people structure

    Parameters
    ----------
    lname: str
        Last name of person to delete

    Returns
    -------
    200
        On successful delete
    401
        If not found
    '''
    # Does the person to delete exist?
    if lname in PEOPLE:
        del PEOPLE[lname]
        return make_response(
            "{lname} successfully deleted".format(lname=lname), 200
        )
    # Otherwise, nope, person to delete not found
    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )
