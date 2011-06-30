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
                self.assertEqual(len(json_objects), expected_length)

    # Test /api/tickets/*
    def test_tickets(self):
        '''Tests: /api/tickets/'''

        self.json_test_helper(['/api/tickets/'], 30)

    def test_tickets_open_closed(self):
        '''Tests: /api/tickets/open/, /api/tickets/closed/, and
        /api/tickets/both'''

        urls = ['/api/tickets/open/', '/api/tickets/closed/',
                '/api/tickets/both/']
        self.json_test_helper(urls, 30)

    def test_tickets_date_range(self):
        '''Tests: /api/tickets/YYYY-MM-DD/YYYY-MM-DD/'''

        random_number = random.randint(1, 90)
        end_date = str(datetime.date.today())
        start_date = str(datetime.date.today()-datetime. \
                timedelta(days=random_number))

        urls = ['/api/tickets/open/%s/%s/' % (start_date, end_date)]
        self.json_test_helper(urls, random_number+1)

    def test_tickets_date_count(self):
        '''Tests: /api/tickets/open/[0-9]+ and
        /api/tickets/oped/YYYY-MM-DD/[0-9]+'''

        random_number = random.randint(1, 90)
        end_date = str(datetime.date.today())

        url_sans_date = ['/api/tickets/open/%s/' % random_number]
        url_date = ['/api/tickets/open/%s/%s/' % (end_date, random_number)]

        self.json_test_helper(url_sans_date, random_number+1)
        self.json_test_helper(url_date, random_number)

