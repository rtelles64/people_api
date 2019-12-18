# This connects to the swagger.yml file:
# We configured Connexion with the operationId value to call the people module
# and the read function within the module when the API gets an HTTP GET
# This means this file must exist and contain a read() function

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
    list
        A sorted list of people
    '''
    # Create list of people from our data
    return [PEOPLE[key] for key in sorted(PEOPLE.keys())]


# Create handler for our read where an lname parameter is provided
def read_one(lname):
    '''
    This function responds to a request for /api/people/{lname} with one
    matching person from people

    Parameters
    ----------
    lname: str
        Last name of person to find

    Returns
    -------
    PEOPLE
        Person matching last name
    '''
    # Does the person exist in people?
    if lname in PEOPLE:
        person = PEOPLE.get(lname)
    # Otherwise, nope, not found
    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )

    return person


def create(person):
    '''
    This function creates a new person in the people structure based on the
    passed in person data

    Parameters
    ----------
    person: PERSON
        Person to create in people structure

    Returns
    -------
    201
        On success
    406
        On person exists
    '''
    lname = person.get("lname", None)
    fname = person.get("fname", None)

    # Does the person exist already?
    if lname not in PEOPLE and lname is not None:
        PEOPLE[lname] = {
            "lname": lname,
            "fname": fname,
            "timestamp": get_timestamp(),
        }

        return make_response(
            "{lname} successfully created".format(lname=lname), 201
        )
    # Otherwise, they exist, that's an error
    else:
        abort(
            406,
            "Person with last name {lname} already exists!".format(lname=lname),
        )


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
