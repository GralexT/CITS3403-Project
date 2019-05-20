import unittest
import os
import time
from app import app, db
from app.models import User, Comparison, Feedback
from selenium import webdriver

basedir = os.path.abspath(os.path.dirname(__file__))


class SystemTest(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=os.path.join(basedir, 'chromedriver'))

        if not self.driver:
            self.driver = webdriver.Chrome(executable_path=os.path.join(basedir, 'geckodriver'))

            if not self.driver:
                self.skipTest('Web browser not available')
        else:
            app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite://' + os.path.join(basedir, 'test.db')
            db.init_app(app)
            db.create_all()
            u1 = User(username='Case', email='Case@gmail.com')
            u2 = User(username='Unit', email='Unit@gmail.com')
            # lab = Lab(lab='test-lab', time='now')
            db.session.add(u1)
            db.session.add(u2)
            # db.session.add(lab)
            db.session.commit()
            self.driver.maximize_window()
            self.driver.get('http://localhost:5000/')

    def tearDown(self):
        if self.driver:
            self.driver.close()
            db.session.query(User).delete()
            db.session.query(Comparison).delete()
            db.session.query(Feedback).delete()
            db.session.commit()
            db.session.remove()

    def test_create_account(self):
        u = User.query.get('2')
        self.assertEqual(u.username, 'Unit', msg='user exists in db')
        self.driver.get('http://localhost:5000/create_account')
        self.driver.implicitly_wait(5)
        username = self.driver.find_element_by_id('username')
        username.send_keys('Test')
        email = self.driver.find_element_by_id('email')
        email.send_keys('Test@gmail.com')
        password = self.driver.find_element_by_id('password')
        password.send_keys('123456')
        password2 = self.driver.find_element_by_id('password2')
        password2.send_keys('123456')
        time.sleep(1)
        self.driver.implicitly_wait(5)
        submit = self.driver.find_element_by_id('submit')
        submit.click()
        # check login success
        self.driver.implicitly_wait(5)
        time.sleep(1)

    def test_login(self):
        u = User.query.get('2')
        self.assertEqual(u.username, 'Unit', msg='user exists in db')
        u.set_password_hash("123456")
        self.driver.get('http://localhost:5000/login')
        self.driver.implicitly_wait(5)
        username = self.driver.find_element_by_id('username')
        username.send_keys('Unit')
        password = self.driver.find_element_by_id('password')
        password.send_keys('123456')
        submit = self.driver.find_element_by_id('submit')
        submit.click()
        time.sleep(1)
        self.driver.implicitly_wait(10)


if __name__ == '__main__':
    unittest.main(verbosity=2)
