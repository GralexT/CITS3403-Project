# CITS3403-Project


## Purpose

The purpose of the web application is to rank and compare subreddits and posts from the website reddit, while collecting publically submitted feedback from users.

## Architecture

Model:
Code reuse is minimal - all code is divided into files named after thier primary functions, i.e, all routes exist in routes.py, models in models.py, forms in forms.py, html in templates, css in /static/styles.
Some functions are designed to take arguments that allow them to be used in different contexts.

View:
Navigation made easy by a sticky navbar that holds all major links. Content manipulation for users with correct permissions may be accessed by links in the content.

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

Unit tests are in the tests folder to run them simply run unittests.py

## Examples of Team Work

Reference file "log.log".

## Dependancies

Reference "Requirements.txt".

Click	7.0	7.0
Flask	1.0.3	1.0.3
Flask-Admin	1.5.3	1.5.3
Flask-Login	0.4.1	0.4.1
Flask-Migrate	2.5.0	2.5.0
Flask-SQLAlchemy	2.4.0	2.4.0
Flask-WTF	0.14.2	0.14.2
Jinja2	2.10.1	2.10.1
Mako	1.0.10	1.0.10
MarkupSafe	1.1.1	1.1.1
SQLAlchemy	1.3.3	1.3.3
WTForm	1.0	1.0
WTForms	2.2.1	2.2.1
Werkzeug	0.15.4	0.15.4
alembic	1.0.10	1.0.10
certifi	2019.3.9	2019.3.9
chardet	3.0.4	3.0.4
idna	2.8	2.8
itsdangerous	1.1.0	1.1.0
pip	19.1.1	19.1.1
python-dateutil	2.8.0	2.8.0
python-editor	1.0.4	1.0.4
requests	2.22.0	2.22.0
selenium	3.141.0	3.141.0
setuptools	41.0.1	41.0.1
six	1.12.0	1.12.0
urllib3	1.25.2	1.25.2
