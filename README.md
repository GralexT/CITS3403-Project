# CITS3403-Project


## Purpose

The purpose of the web application is to rank and compare subreddits and posts from the website reddit, while collecting publically submitted feedback from users.

## Architecture

Model:
Code reuse is minimal - all code is divided into files named after thier primary functions, i.e, all routes exist in routes.py, models in models.py, forms in forms.py, html in templates, css in /static/styles.
Some functions are designed to take arguments that allow them to be used in different contexts.

View:
Navigation made easy by a sticky navbar that holds all major links. Content manipulation for users with correct permissions may be accessed by links by the content.

Controller:
Users can edit their feedback through their account page or the feedback page, using anchor links next to their content.
Admins can use flask-admin for additional tools to access databases.
Admins can delete any feedback from any user with links from the feedback page or using admin tools.
Admins can edit page content on the Home and About pages by using links on the pages or by using admin tools.

## How to Launch
Install all dependancies and follow one of two options:
	
	Option 1: Run app.py through python;
		In your cmd/terminal, navigate to Project directory, where you will find app.py.
		
    Type:	$ python app.py

	Option 2: Export app.py as a flask environment variable and run it through flask.
		In your cmd/terminal, navigate to Project directory, where you will find app.py.

		For Windows OS,
		Type:	> set FLASK_APP=hello
			    > flask run

		
		For Unix systems,
		Type:	$ export FLASK_APP=app.py
			    $ flask run

## How to Test

describe some unit tests for the web application, and how to run them.

## Examples of Team Work

Include commit logs, showing contributions and review from both contributing students

## Dependancies
