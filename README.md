# people_api

A REST API that includes input/output validation using Python 3, Flask, and Connexion, providing Swagger documentation as a bonus. Also included is a simple single page web application that demonstrates using the API with JavaScript, updating the DOM with it.

## Getting Started

My operating system is a Mac so the installation instructions reflect this system. The code editor used was Atom. Most of the files and configurations were provided by [RealPython](https://realpython.com/flask-connexion-rest-api/).

### Installing Git

Git is already installed on MacOS, but these instructions are to ensure we have the latest version:

1. go to [https://git-scm.com/downloads](https://git-scm.com/downloads)
2. download the software for Mac
3. install Git choosing all the default options

Once everything is installed, you should be able to run `git` on the command line. If usage information is displayed, we're good to go!

### First Time Git Configuration
Run each of the following lines on the command line to make sure everything is set up.
```
# sets up Git with your name
git config --global user.name "<Your-Full-Name>"

# sets up Git with your email
git config --global user.email "<your-email-address>"

# makes sure that Git output is colored
git config --global color.ui auto

# displays the original state in a conflict
git config --global merge.conflictstyle diff3

git config --list
```

### Git & Code Editor

The last step of configuration is to get Git working with your code editor. Below is the configuration for Atom. If you use a different editor, then do a quick search on Google for "associate X text editor with Git" (replace the X with the name of your code editor).
```
git config --global core.editor "atom --wait"
```

### Download Virtual Environment configuration

Packages/libraries used in this project are listed in [requirements.txt](https://github.com/rtelles64/people_api/blob/master/requirements.txt)

## Version

This project uses `Python 3`

## Run server.py

With packages installed run:

```
python server.py
```

or, if this doesn't work:

```
python3 server.py
```

### Visit localhost:5000/

With the application running, visit `http://localhost:5000` on your favorite browser to test out the app.

## Exit the App

To exit the app, on your keyboard press `control + c`.

## Issues
### ValueError

There is a known error within the [models.py](https://github.com/rtelles64/people_api/blob/master/models.py) file that raises a ValueError in connection with the Marshmallow.ModelSchema setup.

Known error:

`ValueError: Invalid fields for <NotePersonSchema(many=False)>: {'notes'}.`

## Author(s)

* **Roy Telles, Jr.** *(with the help of the RealPython team)*

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/realpython/materials/blob/master/LICENSE) file for details

## Acknowledgments

* I would like to acknowledge and give big thanks to the RealPython team
