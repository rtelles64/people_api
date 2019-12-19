# This gets the necessary modules imported into the program and configured. It
# is used by both build_database.py and server.py

import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# This points to the directory the program is running in
basedir = os.path.abspath(os.path.dirname(__file__))

# Create the Connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

# Configure the SQLAlchemy part of the app instance:
# SQLALCHEMY_ECHO = True
# - causes SQLAlchemy to echo SQL statements to the console (useful to debug
#   problems when building database programs)
# - Set to False for production environments
app.config['SQLALCHEMY_ECHO'] = True
# SQLALCHEMY_DATABASE_URI
# - sqlite://// - tells SQLAlchemy to use SQLite as the database
# - people.db - the database file
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:////' +
                                         os.path.join(basedir, 'people.db'))
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# - Turns off SQLAlchemy event system
# - The event system generates events useful in event-driven programs but adds
#   significant overhead (since this isn't an event-driven program, turn off)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
# This initializes SQLAlchemy by passing the app configuration information
# The db variable is what gets imported into build_database.py to give it
# access to SQLAlchemy and the database. It serves the same purpose in the
# server.py program and people.py module
db = SQLAlchemy(app)

# Initialize Marshmallow
# This allows Marshmallow to introspect the SQLAlchemy components attached to
# the app (this is why it is initialized after SQLAlchemy)
ma = Marshmallow(app)
