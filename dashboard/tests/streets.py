from django.test.simple import TestCase
from django.test.client import Client

from pymongo.connection import Connection

from settings import MONGODB

# Set up the database connection as a global variable
connection = Connection(MONGODB['host'])
db = connection[MONGODB['db']]

class StreetListTest(TestCase):
    """ Test /street/ """

    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/street/')

    def test_success(self):
        """ GET /street/ should return status_code 200 """
        self.assertEquals(self.response.status_code, 200)

    def test_templates(self):
        """ GET /street/ should use the correct templates """
        self.assertTemplateUsed(self.response, 'street_list.html')

    def test_redirect(self):
        """ GET /street should return status_code 301 """
        response = self.client.get('/street')
        self.assertEquals(response.status_code, 301)

class StreetSpecificTest(TestCase):
    """ Test /street/__slug__/ """

    def setUp(self):
        self.client = Client()

        # Find a single street.
        street = db.streets.find_one()

        try:
            self.slug = street['properties']['slug']
        except:
            error = "No slug found for '%s'" % street['properties']['name']
            raise KeyError(error)

        self.response = self.client.get('/street/%s/' % self.slug)

    def test_success(self):
        """ GET /street/__slug__/ should return status_code 200 """
        self.assertEquals(self.response.status_code, 200)

    def test_templates(self):
        """ GET /street/__slug__/ shoudl use the correct templates """
        self.assertTemplateUsed(self.response, 'street_list.html')

    def test_redirect(self):
        """ GET /street/__slug__ should return status_code 301 """
        response = self.client.get('/street/%s' % self.slug)
        self.assertEquals(response.status_code, 301)

class StreetDetailTest(TestCase):
    """ Test /street/__slug__/ """

    def setUp(self):
        self.client = Client()

        street = db.streets.find_one()

        try:
            self.slug = street['properties']['slug']
        except:
            error = "No slug found for '%s'" % street['properties']['name']
            raise KeyError(error)

        self.min = street['properties']['min']
        self.max = street['properties']['max']

        self.response = self.client.get('/street/%s/%d-%d/' %
                (self.slug, self.min, self.max))

    def test_success(self):
        """ GET /street/__slug__/##-##/ should return status_code 200 """
        self.assertEquals(self.response.status_code, 200)

    def test_templates(self):
        """ GET /street/__slug__/##-##/ should use the correct templates """
        self.assertTemplateUsed(self.response, 'geo_detail.html')

    def test_context(self):
        """ GET /street/__slug__/##-##/ should use the correct context
        variables"""
        self.assertTrue('title' in self.response.context)
        self.assertTrue('geometry' in self.response.context)
        self.assertTrue('centroid' in self.response.context)
        self.assertTrue('extent' in self.response.context)
        self.assertTrue('stats' in self.response.context)
        self.assertTrue('nearby' in self.response.context)
        self.assertTrue('type' in self.response.context)
        self.assertTrue('id' in self.response.context)

    def test_redirect(self):
        """ GET /street/__slug__/##-## should return status_code 301 """
        response = self.client.get('/street/%s/%d-%d' %
                (self.slug, self.min, self.max))
        self.assertEquals(response.status_code, 301)

