from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, current_user
from app import db, login, admin, ModelView, expose, Admin, AdminIndexView


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean)

    feedback = db.relationship('Feedback', backref='user', lazy=True)

    def __repr__(self):
        return '<User: {}, Email: {}, isAdmin: {}>'.format(self.username, self.email, self.admin)

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

    def get_password_reset_token(self, espires_sec=600):
        serializer = Serializer(app.config['SECRET_KEY'], time)
        return serializer.dumps({'uid':self.id}).decode('utf-8')

    @staticmethod
    def verify_password_reset_token(token):
        serializer = Serializer(app.condig['SECRET_KEY'])
        try:
            uid = serializer.loads(token)['uid']
        except:
            return None
        return User.query.get(uid)


class Home(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    heading = db.Column(db.String())
    text = db.Column(db.Text)

    def __repr__(self):
        return '<Home: {}, Title: {}>'.format(self.key, self.title)


class About(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    heading = db.Column(db.String())
    text = db.Column(db.Text)

    def __repr__(self):
        return '<About: {}, Title: {}>'.format(self.key, self.title)


class Comparison(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    subreddit = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(120))
    timescale = db.Column(db.String(120))
    colours = db.Column(db.String(120))

    def __repr__(self):
        return '<Comparison: {}>'.format(self.key)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    title = db.Column(db.String())
    text = db.Column(db.Text)

    def __repr__(self):
        return '<UserID: {}, Timestamp: {}, Title: {}>'.format(self.uid, self.timestamp, self.title)
        

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Admin Models.
class AccessibleView(ModelView):
    def is_accessible(self):
        return current_user.admin

class UserView(ModelView):
    form_columns = ['id', 'username', 'email', 'admin', 'feedback']

    def is_accessible(self):
        return current_user.admin



@login.user_loader
def load_user(id):
    return User.query.get(int(id))


admin.add_view(UserView(User, db.session))
admin.add_view(AccessibleView(Home, db.session))
admin.add_view(AccessibleView(About, db.session))
admin.add_view(AccessibleView(Comparison, db.session))
admin.add_view(AccessibleView(Feedback, db.session))

