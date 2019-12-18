from flask import Flask, render_template

import connexion

# Create application instance
# USING FLASK
# app = Flask(__name__, template_folder="templates")

# USING CONNECTION
app = connexion.App(__name__, specification_dir='./')

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')

# Create URL route for "/"
@app.route('/')
def home():
    '''
    Just reponds to the browser URL

    Returns
    -------
    str
        The rendered template 'home.html'
    '''
    return render_template('home.html')


# If running in stand alone mode, run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
