from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm


@app.route("/")
@app.route("/home")
def home():
  return render_template('home.html')


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/compare")
def compare():
    return render_template("compare.html")


@app.route("/top_ranks")
def topRanks():
    return render_template("top_ranks.html")


@app.route("/account")
def account():
    return render_template("account.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('account'))
    return render_template('login.html', title='Sign In', form=form)

