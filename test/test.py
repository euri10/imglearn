__author__ = 'euri10'
from imglearn import app, db, User

import unittest


class FlaskTestCase(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_register_user_already_exists(self):
        tester = app.test_client(self)
        response = tester.post('/register',
                               data=dict(email='benoit.barthelet@gmail.com', password='thisisatest',
                                         confirm='thisisatest'),
                               follow_redirects=True)
        self.assertTrue(b'user already exists' in response.data)

    def test_register_password_dont_match(self):
        user = User(email='toto@test.com', password='azerty')
        if user is not None:
            User.query.filter(User.email == 'toto@test.com').delete()
            db.session.commit()
        tester = app.test_client(self)
        response = tester.post('/register',
                               data=dict(email='toto@test.com', password='thisisatest', confirm='aaaaaa'),
                               follow_redirects=True)
        self.assertTrue(b'Please repeat password' in response.data)

    def test_register(self):
        user = User(email='toto@test.com', password='azerty')
        if user is not None:
            User.query.filter(User.email == 'toto@test.com').delete()
            db.session.commit()
        tester = app.test_client(self)
        response = tester.post('/register',
                               data=dict(email='toto@test.com', password='azerty', confirm='azerty'),
                               follow_redirects=True)

        self.assertTrue(b'Thanks for registering' in response.data)


if __name__ == '__main__':
    unittest.main()