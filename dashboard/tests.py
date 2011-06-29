from django.test import TestCase
from django.utils import unittest
from django.test.client import Client

import datetime
import json
import random

class ApiTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def json_test_helper(self, urls, expected_length=None):
        '''Helper method that runs through a list of URLs to check the length
        of the response'''

        for url in urls:
            # Check the response code.
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

            json_objects = json.loads(response.content)

            # If expected_length is set, check it.
            if expected_length is not None:
                self.assertEqual(len(json_objects, expected_length))

    def test_tickets(self):
        self.json_test_helper(['/api/tickets/'], 30)


    def test_tickets_opened_closed(self):
        urls = ['/api/tickets/opened/', '/api/tickets/closed/']
        self.json_test_helper(urls, 30)

    def test_tickets_date_range(self):
        random_number = random.randint(1, 90)
        end_date = str(datetime.date.today())
        start_date = str(datetime.date.today()-datetime. \
                timedelta(days=random_number))

        urls = ['/api/tickets/opened/%s/%s/' % (start_date, end_date)]
        self.json_test_helper(urls, random_number+1)

    def test_tickets_date_count(self):
        random_number = random.randint(1, 90)
        end_date = str(datetime.date.today())

        url_sans_date = ['/api/tickets/opened/%s/' % random_number]
        url_date = ['/api/tickets/opened/%s/%s/' % (end_date, random_number)]

        self.json_test_helper(url_sans_date, random_number+1)
        self.json_test_helper(url_date, random_number)

