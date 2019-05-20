from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, regexp, EqualTo, Email, ValidationError, Length
from app.models import User
import requests

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class CreateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class UpdateUsernameForm(FlaskForm):
    username = StringField('Change Username', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class RequestChangePasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Email entered is not a registered account.')


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class FeedbackForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    feedback = TextAreaField('Feedback', validators=[DataRequired()])
    submit = SubmitField('Submit Feedback')


class SectionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    heading = StringField('Heading')
    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CompareForm(FlaskForm):
    subreddit1 = StringField(validators=[DataRequired()], render_kw={"placeholder": "First Subreddit"})
    subreddit2 = StringField(render_kw={"placeholder": "Second Subreddit (Optional)"})
    submit = SubmitField('Compare Subreddits')

    def validate_subreddit1(self, subreddit1):
        response = requests.get("https://www.reddit.com/subreddits/search.json?q="+subreddit1.data+"?",
                                headers={'User-agent': 'my bot 0.1'})
        data = response.json()
        if len(data["data"]["children"]) is 0:
            raise ValidationError('Could not find any subreddits by that name, please try something else.')

    def validate_subreddit2(self, subreddit2):
        if subreddit2.data:
            response = requests.get("https://www.reddit.com/subreddits/search.json?q="+subreddit2.data+"?",
                                    headers={'User-agent': 'my bot 0.1'})
            data = response.json()
            if len(data["data"]["children"]) is 0:
                raise ValidationError('Could not find any subreddits by that name, please try something else.')

