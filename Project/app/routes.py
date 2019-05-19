from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from sqlalchemy import desc

from app import app, db
from app.forms import LoginForm, CreateAccountForm, UpdateUsernameForm, FeedbackForm, SectionForm
from app.models import User, Comparison, Feedback, Home, About


@app.route("/")
@app.route("/home")
def home():
    sections = Home.query.all()
    return render_template('home.html', sections=sections)


@app.route("/about")
def about():
    sections = About.query.all()
    return render_template("about.html", title='About', sections=sections)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Sections are the material contained in the Home and About pages.
@app.route("/section/new/<string:currentpage>", methods=['GET', 'POST'])
@login_required
def new_section(currentpage):
    if not current_user.admin:
        abort(403)
    form = SectionForm()
    if form.validate_on_submit():
        if currentpage == 'home':
            newsection = Home(title=form.title.data, heading=form.heading.data, text=form.text.data)
        else:
            newsection = About(title=form.title.data, heading=form.heading.data, text=form.text.data)
        db.session.add(newsection)
        db.session.commit()
        flash('Section Updated.')
        return redirect(url_for(currentpage))
    return render_template('section_form.html', title='New Section', form=form)


@app.route("/section/update/<int:sectionId><string:currentpage>", methods=['GET', 'POST'])
@login_required
def update_section(sectionId, currentpage):
    if not current_user.admin:
        abort(403)
    if currentpage == 'home':
        section = Home.query.get_or_404(sectionId)
    else:
        section = About.query.get_or_404(sectionId)
    form = SectionForm()
    if form.validate_on_submit():
        section.title = form.title.data
        section.heading = form.heading.data
        section.text = form.text.data
        db.session.commit()
        flash('Section Updated.')
        return redirect(url_for(currentpage))
    form.title.data = section.title
    form.heading.data = section.heading
    form.text.data = section.text
    return render_template('section_form.html', title='Update Section', form=form)


@app.route("/section/delete/<int:sectionId><string:currentpage>", methods=['GET', 'POST'])
@login_required
def delete_section(sectionId, currentpage):
    if not current_user.admin:
        abort(403)
    if currentpage == 'home':
        section = Home.query.get_or_404(sectionId)
    else:
        section = About.query.get_or_404(sectionId)
    db.session.delete(section)
    db.session.commit()
    flash('Section Deleted.')
    return redirect(url_for(currentpage))


@app.route("/compare")
def compare():
    return render_template("compare.html", title='Compare')


@app.route("/top_ranks")
def topRanks():
    return render_template("top_ranks.html", title='Top Ranks')

@app.route("/feedback")
def feedback():
    page = request.args.get('page', 1, type=int)
    feedback = Feedback.query.order_by(desc(Feedback.timestamp)).paginate(page=page, per_page=5)
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
    return render_template('new_feedback.html', title='Your Feedback', form=form, legend='New Feedback')


@app.route("/feedback/update/<int:feedbackId><string:currentpage>", methods=['GET', 'POST'])
@login_required
def update_feedback(feedbackId, currentpage):
    feedback = Feedback.query.get_or_404(feedbackId)
    if feedback.uid != current_user.id:
        abort(403)
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.text = form.feedback.data
        db.session.commit()
        flash('Feedback Updated.')
        return redirect(url_for(currentpage))
    form.title.data = feedback.title
    form.feedback.data = feedback.text
    return render_template('new_feedback.html', title='Update Feedback', form=form, legend='Update Feedback')


@app.route("/feedback/delete/<int:feedbackId><string:currentpage>", methods=['GET', 'POST'])
@login_required
def delete_feedback(feedbackId, currentpage):
    feedback = Feedback.query.get_or_404(feedbackId)
    if feedback.uid != current_user.id:
        abort(403)
    db.session.delete(feedback)
    db.session.commit()
    flash('Feedback Deleted.')
    return redirect(url_for(currentpage))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUsernameForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Username changed.')
        return redirect(url_for('account'))
    page = request.args.get('page', 1, type=int)
    feedback = Feedback.query.filter_by(user=current_user).order_by(desc(Feedback.timestamp)).paginate(page=page, per_page=2)
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


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Please follow the link sent to your email to reset your password.')
        return redirect(url_for('login'))
    return render_template("reset_password.html", title='Reset Password - Email Required', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    user = User.verify_reset_token(token)
    if not user:
        flash('Invalid token.')
        return redirect(url_for('reset_password'))
    form = ResetPasswordForm()
    return render_template("reset_token.html", title='Reset Password', form=form)


@app.route("/admin")
def admin():
    return render_template('admin_home.html')
