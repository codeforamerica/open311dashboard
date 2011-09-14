from django.test.simple import TestCase
from django.test.client import Client

from pymongo.connection import Connection

from settings import MONGODB

# Set up the database connection as a global variable
connection = Connection(MONGODB['host'])
db = connection[MONGODB['db']]
class NeighborhoodListTest(TestCase):
    """ Test /neighborhood/ """

    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/neighborhood/')

    def test_success(self):
        """ GET /neighborhood/ should return status_code 200 """
        self.assertEquals(self.response.status_code, 200)

    def test_templates(self):
        """ GET /neighborhood/ should use the correct templates """
        self.assertTemplateUsed(self.response, 'neighborhood_list.html')

    def test_context(self):
        """ GET /neighborhood/ should use the correct context variables """
        self.assertTrue('neighborhoods' in self.response.context)

    def test_redirect(self):
        """ GET /neighborhood should return status_code 301 """
        response = self.client.get('/neighborhood')
        self.assertEquals(response.status_code, 301)

class NeighborhoodDetailTest(TestCase):
    """ Test /neighborhood/__slug__/ """

    def setUp(self):
        self.client = Client()

        # Find a single neighborhood.
        neighborhood = db.polygons.find_one({ 'properties.type' :
            'neighborhood'})
        try:
            self.slug = neighborhood['properties']['slug']
        except:
            error =  "No slug found for '%s'" \
                    % neighborhood['properties']['name']
            raise KeyError(error)

        self.response = self.client.get('/neighborhood/%s/' % self.slug)

    def test_success(self):
        """ GET /neighborhood/__slug__/ should return status_code 200 """
        self.assertEquals(self.response.status_code, 200)

    def test_templates(self):
        """ GET /neighborhood/__slug__/ should use the correct templates """
        self.assertTemplateUsed(self.response, 'geo_detail.html')

    def test_context(self):
        """ GET /neighborhood/__slug__/ should use the correct context
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
        """ GET /neighborhood/__slug__ should return status_code 304 """
        response = self.client.get('/neighborhood/%s' % self.slug)
        self.assertEquals(response.status_code, 301)


