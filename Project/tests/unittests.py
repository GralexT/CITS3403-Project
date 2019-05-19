import unittest, os
from app import app, db
from app.models import User, Comparison, Feedback


class UserModelCase(unittest.TestCase):

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite://'+os.path.join(basedir, 'test.db')
        self.app = app.test_client()  # creates a virtual test environment
        db.create_all()
        u1 = User(username='Case', email='Case@gmail.com')
        u2 = User(username='Test', email='Test@gmail.com')
        # lab = Lab(lab='test-lab',time='now')
        db.session.add(u1)
        db.session.add(u2)
        # db.session.add(lab)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User.query.get('1')
        u.set_password_hash('test')
        self.assertFalse(u.check_password_hash('case'))
        self.assertTrue(u.check_password_hash('test'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
