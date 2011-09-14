from django.test.simple import TestCase
from django.test.client import Client

from pymongo.connection import Connection

from settings import MONGODB

# Set up the database connection as a global variable
connection = Connection(MONGODB['host'])
db = connection[MONGODB['db']]

class IndexTest(TestCase):
    """ Test / """

    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/')

    def test_success(self):
        """ GET / should return status_code 200 """
        self.assertEquals(self.response.status_code, 200)

    def test_templates(self):
        """ GET / should use the correct templates """
        self.assertTemplateUsed(self.response, 'index.html')

    def test_context(self):
        """ GET / should use the correct context variables """
        self.assertTrue('open_tickets' in self.response.context)
        self.assertTrue('this_week_stats' in self.response.context)
        self.assertTrue('last_week_stats' in self.response.context)
        self.assertTrue('delta' in self.response.context)

