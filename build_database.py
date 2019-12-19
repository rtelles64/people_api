# A utility program to create and build the database with the People data

import os

from config import db
from models import Person

# Data to initialize database with
PEOPLE = [
    {'fname': 'Doug', 'lname': 'Farrell'},
    {'fname': 'Kent', 'lname': 'Brockman'},
    {'fname': 'Bunny', 'lname': 'Easter'}
]

# Delete database file if it exists currently
# If you have to re-initialize the database to get a clean start, this makes
# sure you're starting from scratch
if os.path.exists('people.db'):
    os.remove('people.db')

# Create the database
db.create_all()

# Iterate over the PEOPLE structure and populate the database
for person in PEOPLE:
    p = Person(lname=person['lname'], fname=person['fname'])
    db.session.add(p)

# At this point no data is added to the database, but is saved within the
# session object. Only when db.session.commit() is called does the session
# interact with the database and commit the actions to it.
db.session.commit()
