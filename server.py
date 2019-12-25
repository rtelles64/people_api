from flask import render_template

import config

# Create application instance
# USING FLASK
# app = Flask(__name__, template_folder="templates")

# USING CONNECTION
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api('swagger.yml')


# Create URL route for "/"
@connex_app.route('/')
def home():
    '''
    Just reponds to the browser URL localhost:5000/

    Returns
    -------
    str
        The rendered template 'home.html'
    '''
    return render_template('home.html')


# Create URL route for '/people'
@connex_app.route('/people')
@connex_app.route('/people/<int:person_id>')
def people(person_id=''):
    '''
    This function responds to the URL localhost:5000/people

    Parameters
    ----------
    person_id : int, optional
        Id of the person to retrieve (default is empty)

    Returns
    -------
    str
        The rendered template 'people.html'
    '''
    return render_template('people.html', person_id=person_id)


# Create URL for notes
@connex_app.route('/people/<int:person_id>')
@connex_app.route('/people/<int:person_id>/notes')
@connex_app.route('/people/<int:person_id>/notes/<int:note_id>')
def notes(person_id, note_id=''):
    '''
    This function responds to the URL localhost:5000/notes/<person_id>

    Parameters
    ----------
    person_id : int
        Id of person to retrieve
    note_id : int, optional
        Id of note to view (default is empty)
    '''
    return render_template('notes.html', person_id=person_id, note_id=note_id)


# If running in stand alone mode, run the app
if __name__ == '__main__':
    connex_app.run(debug=True)
