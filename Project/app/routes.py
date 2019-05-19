from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
import requests

from app import app, db
from app.forms import LoginForm, CreateAccountForm, CompareForm
from app.models import User


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template("about.html", title='About')


# needs to check if subreddit is private before request data about the subreddit
@app.route('/compare', methods=['GET', 'POST'])
def compare():
    form = CompareForm()
    if form.validate_on_submit():
        response = requests.get("https://www.reddit.com/subreddits/search.json?q=" + form.subreddit1.data,
                                headers={'User-agent': 'my bot 0.1'}).json()
        subreddit1_display_name = response["data"]["children"][0]["data"]["display_name_prefixed"]
        data1 = requests.get('https://www.reddit.com/'+subreddit1_display_name+'/about.json',
                             headers={"User-agent": 'my bot 0.1'}).json()
        data2 = ""
        flash('Appropriate Subreddit was found, ' + subreddit1_display_name)

        if form.subreddit2.data:
            response = requests.get("https://www.reddit.com/subreddits/search.json?q=" + form.subreddit2.data,
                                    headers={'User-agent': 'my bot 0.1'}).json()
            subreddit2_display_name = response["data"]["children"][0]["data"]["display_name_prefixed"]
            data2 = requests.get('https://www.reddit.com/'+subreddit2_display_name+'/about.json',
                                 headers={"User-agent": 'my bot 0.1'}).json()
            flash('Appropriate Subreddit was found, ' + subreddit2_display_name)

        return render_template("compare_filled.html", title='Compare Filled', form=form,
                               sub1_data=data1,
                               sub2_data=data2)
    return render_template("compare.html", title='Compare', form=form)


@app.route("/top_ranks")
def topRanks():
    response = requests.get("https://www.reddit.com/r/all/top.json?t=all", headers={'User-agent':'my bot 0.1'}).json()
    post_popular = response["data"]["children"]
    post_popular_len = len(post_popular)
    return render_template("top_ranks.html", title='Top Ranks',
                           post_popular=post_popular,
                           post_popular_len=post_popular_len)


@app.route("/feedback")
def feedback():
    return render_template("feedback.html", title='Feedback')


@app.route("/account")
def account():
    return render_template("account.html", title='Account')


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
        return redirect(url_for('home'))
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