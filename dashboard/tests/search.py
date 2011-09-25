from django.test.simple import TestCase
from django.test.client import Client

from pymongo.connection import Connection

from settings import MONGODB

# Set up the database connection as a global variable
connection = Connection(MONGODB['host'])
db = connection[MONGODB['db']]

class SearchTest(TestCase):
    """ Test /search/ """

    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/search/')

    def test_success(self):
        """ GET /search/ should return status_code 200 """
        self.assertEquals(self.response.status_code, 200)

    def test_templates(self):
        """ GET /search/ should use the correct templates """
        self.assertTemplateUsed(self.response, 'search.html')

    def test_search(self):
        """ GET /search/?q=85+2nd+st should work correctly"""
        response = self.client.get('/search/', {'q' : '85 2nd st.'})
        self.assertEquals(response.status_code, 302)

    def test_redirect(self):
        """ GET /search should return status_code 301 """
        response = self.client.get('/search')
        self.assertEquals(response.status_code, 301)

