__author__ = 'euri10'
from imglearn import app


import unittest

class FlaskTestCase(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        pass

if __name__ == '__main__':
    unittest.main()