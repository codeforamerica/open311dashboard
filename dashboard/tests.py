from django.test import TestCase

import json
import random

class IndexTest(TestCase):
    """Test the index view and related json"""
    fixtures = ['test.json']

    def test_success(self):
        """Test that the index works"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        """Test that the correct templates are being rendered"""
        response = self.client.get("/")
        self.assertTemplateUsed(response, 'index.html')
        self.assertTemplateUsed(response, 'base/main.html')

    def test_api_success(self):
        """Test the JSON API"""
        rand = random.randint(1,5)
        response = self.client.get("/api/home/%s.json" % rand)

        self.assertEqual(response.status_code, 200)

    def test_api_valid(self):
        """Test that the JSON is valid"""
        rand = random.randint(1,5)
        response = self.client.get("/api/home/%s.json" % rand)
        data = json.loads(response.content)

        self.assertIsInstance(data, dict)

class NeighborhoodTest(TestCase):
    """Test the neighborhood views"""
    fixtures = ['test.json']

    def test_success_list(self):
        """Check to make sure the neighborhood list is working"""
        response = self.client.get("/neighborhood/")
        self.assertEqual(response.status_code, 200)

    def test_success_detail(self):
        """Check to make sure neighborhood detail is working"""
        rand = random.randint(1, 5)
        response = self.client.get("/neighborhood/%s/" % rand)

        self.assertEqual(response.status_code, 200)

    def test_success_api(self):
        """Check to make sure the API works"""
        rand = random.randint(1, 5)
        response = self.client.get("/neighborhood/%s.json" % rand)
        self.assertEqual(response.status_code, 200)

    def test_template_list(self):
        """Check the template that is rendered for the neighborhood list."""
        response = self.client.get("/neighborhood/")
        self.assertTemplateUsed(response, "neighborhood_list.html")
        self.assertTemplateUsed(response, "base/main.html")

    def test_template_detail(self):
        """Check the template that is rendered for the neighborhood detail."""
        rand = random.randint(1, 5)
        response = self.client.get("/neighborhood/%s/" % rand)

        self.assertTemplateUsed(response, "geo_detail.html")
        self.assertTemplateUsed(response, "base/main.html")

    def test_redirect_list(self):
        """Check the neighborhood list redirect"""
        response = self.client.get("/neighborhood")
        self.assertEqual(response.status_code, 301)

    def test_redirect_detail(self):
        """Check the neighborhood detail redirect"""
        rand = random.randint(1, 5)
        response = self.client.get("/neighborhood/%s" % rand)
        self.assertEqual(response.status_code, 301)

    def test_valid_api(self):
        """Make sure the neighborhood detail api is working"""
        rand = random.randint(1, 5)
        response = self.client.get("/neighborhood/%s.json" % rand)
        data = json.loads(response.content)

        self.assertIsInstance(data, list)

class StreetTest(TestCase):
    """Test the street pages"""
    fixtures = ['test.json']
    def test_success_list(self):
        """Check that the street list works"""
        response = self.client.get("/street/")
        self.assertEqual(response.status_code, 200)

    def test_success_detail(self):
        """Check that the street detail is working"""
        rand = random.randint(2, 50)
        response = self.client.get("/street/%s/" % rand)
        self.assertEqual(response.status_code, 200)

    def test_success_api(self):
        """Check that the street api is working"""
        rand = random.randint(2, 50)
        response = self.client.get("/street/%s.json" % rand)
        self.assertEqual(response.status_code, 200)

    def test_template_list(self):
        """Check the street list templates"""
        response = self.client.get("/street/")
        self.assertTemplateUsed(response, "street_list.html")
        self.assertTemplateUsed(response, "base/main.html")

    def test_template_detail(self):
        """Check the street detail templates"""
        rand = random.randint(2, 50)
        response = self.client.get("/street/%s/" % rand)
        self.assertTemplateUsed(response, "geo_detail.html")
        self.assertTemplateUsed(response, "base/main.html")

    def test_redirect_list(self):
        """Check street list redirect"""
        response = self.client.get("/street")
        self.assertEqual(response.status_code, 301)

    def test_redirect_detail(self):
        """Check street detail redirect"""
        rand = random.randint(2, 50)
        response = self.client.get("/street/%s" % rand)
        self.assertEqual(response.status_code, 301)

    def test_valid_api(self):
        """Check that the API is valid"""
        rand = random.randint(2, 50)
        response = self.client.get("/street/%s.json" % rand)
        data = json.loads(response.content)
        self.assertIsInstance(data, list)

class SearchTest(TestCase):
    """Test the search"""

    def test_success_search(self):
        """Check for success rendering the status page"""
        response = self.client.get("/search/")
        self.assertEqual(response.status_code, 200)

    def test_template_search(self):
        """Check the template rendered on the search page"""
        response = self.client.get("/search/")
        self.assertTemplateUsed(response, "search.html")
        self.assertTemplateUsed(response, "base/main.html")

    def test_redirect_search(self):
        """Check the redirect on the search page"""
        response = self.client.get("/search")
        self.assertEqual(response.status_code, 301)

class MapTest(TestCase):
    def test_success_map(self):
        """Check that the map page works"""
        response = self.client.get("/map/")
        self.assertEqual(response.status_code, 200)

    def test_template_map(self):
        """Check the templates rendered on the map page"""
        response = self.client.get("/map/")
        self.assertTemplateUsed(response, "map.html")
        self.assertTemplateUsed(response, "base/main.html")

    def test_redirect_map(self):
        """Check that the redirect works on the map page"""
        response = self.client.get("/map")
        self.assertEqual(response.status_code, 301)
