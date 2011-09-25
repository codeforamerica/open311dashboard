from django.test.simple import TestCase
from django.test.client import Client

from pymongo.connection import Connection

from settings import MONGODB

# Set up the database connection as a global variable
connection = Connection(MONGODB['host'])
db = connection[MONGODB['db']]

class MapTest(TestCase):
    """ Test /map/ """

    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/map/')

    def test_success(self):
        """ GET /map/ should return status_code 200 """
        self.assertEquals(self.response.status_code, 200)

    def test_templates(self):
        """ GET /map/ should use the correct templates """
        self.assertTemplateUsed(self.response, 'map.html')

    def test_redirect(self):
        """ GET /map should return status_code 301 """
        response = self.client.get('/map')
        self.assertEquals(response.status_code, 301)
