try:
    import simplejson as json
except:
    import json

from django.test.simple import TestCase

from pymongo.connection import Connection

from settings import MONGODB

# Set up the database connection as a global variable
connection = Connection(MONGODB['host'])
db = connection[MONGODB['db']]

class ApiTestCase(TestCase):
    def assertGeoJson(self, content):
        """ Check if the content is valid GeoJSON """
        geojson = json.loads(content)

        self.assertTrue('type' in geojson)
        self.assertTrue('features' in geojson)

        for feature in geojson['features']:
            self.assertTrue('properties' in feature)
            self.assertTrue('geometry' in feature)

class ApiPolygonTest(ApiTestCase):
    """ Test the API handler for polygons. """
    def setUp(self):
        self.base = '/api/polygons/'

    def test_success(self):
        """ GET /api/polygons/ should return status_code 200 """
        response = self.client.get(self.base)
        self.assertEquals(response.status_code, 200)

    def test_redirect(self):
        """ GET /api/polygons should return status_code 301 """
        response = self.client.get('/api/polygons')
        self.assertEquals(response.status_code, 301)

    def test_geojson(self):
        """ GET /api/polygons/ should return valid geojson """
        response = self.client.get(self.base)
        self.assertGeoJson(response.content)

    def test_page_size(self):
        """ GET /api/polygons/?page_size=10 should return the correct
        page size """
        response = self.client.get(self.base,
                {'page_size' : 10 })
        data = json.loads(response.content)
        self.assertTrue(len(data['features']) == 10)

    def test_default_page_size(self):
        """ GET /api/polygons/ should not be larger than 1000 rows """
        response = self.client.get(self.base)
        data = json.loads(response.content)
        self.assertTrue(len(data['features']) <= 1000)

class ApiStreetTest(ApiTestCase):
    """ Test the API handler for streets. """
    def setUp(self):
        self.base = '/api/streets/'

    def test_success(self):
        """ GET /api/streets/ should return status_code 200 """
        response = self.client.get(self.base)
        self.assertEquals(response.status_code, 200)

    def test_redirect(self):
        """ GET /api/streets should return status_code 301 """
        response = self.client.get('/api/streets')
        self.assertEquals(response.status_code, 301)

    def test_geojson(self):
        """ GET /api/streets/ should return valid geojson """
        response = self.client.get(self.base)
        self.assertGeoJson(response.content)

    def test_page_size(self):
        """ GET /api/streets/?page_size=10 should return the correct
        page size """
        response = self.client.get(self.base,
                {'page_size' : 10 })
        data = json.loads(response.content)
        self.assertTrue(len(data['features']) == 10)

    def test_default_page_size(self):
        """ GET /api/streets/ should not be larger than 1000 rows """
        response = self.client.get(self.base)
        data = json.loads(response.content)
        self.assertTrue(len(data['features']) <= 1000)

class ApiRequestTest(ApiTestCase):
    """ Test the API handler for requests. """
    def setUp(self):
        self.base = '/api/requests/'

    def test_success(self):
        """ GET /api/requests/ should return status_code 200 """
        response = self.client.get(self.base)
        self.assertEquals(response.status_code, 200)

    def test_redirect(self):
        """ GET /api/requests should return status_code 301 """
        response = self.client.get('/api/requests')
        self.assertEquals(response.status_code, 301)

    def test_page_size(self):
        """ GET /api/streets/?page_size=10 should return the correct
        page size """
        response = self.client.get(self.base,
                {'page_size' : 10 })
        data = json.loads(response.content)
        self.assertTrue(len(data) == 10)

    def test_default_page_size(self):
        """ GET /api/streets/ should not be larger than 1000 rows """
        response = self.client.get(self.base)
        data = json.loads(response.content)
        self.assertTrue(len(data) <= 1000)
