from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from sqlalchemy import desc

from app import app, db
from app.forms import LoginForm, CreateAccountForm, UpdateUsernameForm, FeedbackForm
from app.models import User, Comparison, Feedback


@app.route("/")
@app.route("/home")
def home():
  return render_template('home.html')


@app.route("/about")
def about():
    return render_template("about.html", title='About')


@app.route("/compare")
def compare():
    return render_template("compare.html", title='Compare')


@app.route("/top_ranks")
def topRanks():
    return render_template("top_ranks.html", title='Top Ranks')

@app.route("/feedback")
def feedback():
    feedback = Feedback.query.order_by(desc(Feedback.timestamp)).limit(25).all()
    return render_template("feedback.html", title='Feedback', feedback=feedback)

@app.route("/feedback/new", methods=['GET', 'POST'])
@login_required
def new_feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(user=current_user, uid=current_user.id, title=form.title.data, text=form.feedback.data)
        db.session.add(feedback)
        db.session.commit()
        flash('Thank you for four feedback.')
        return redirect(url_for('feedback'))
    return render_template('new_feedback.html', title='Your Feedback', form=form)


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUsernameForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Username changed.')
        return redirect(url_for('account'))
    feedback = Feedback.query.filter_by(user=current_user).order_by(desc(Feedback.timestamp)).limit(25).all()
    return render_template("account.html", title='Account', form=form, feedback=feedback)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password_hash(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('account')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = CreateAccountForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Congratulations, you now have an Account!')
        return redirect(url_for('account'))
    return render_template('create_account.html', title='Create Account', form=form)


@app.route("/password_recovery")
def password_recovery():
    return render_template("password_recovery.html", title='Password Recovery')