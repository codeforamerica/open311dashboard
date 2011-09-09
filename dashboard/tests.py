"""
Run tests.

We can't use django's build in TestCase because it requires a database so we're
using unittest.TestCase
"""
# from unittest import TestCase
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

