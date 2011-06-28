from django.test import TestCase
from django.utils import unittest
from django.test.client import Client

import json

class ApiTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_tickets(self):
        response = self.client.get('/api/tickets/')

        self.assertEqual(response.status_code, 200)

        tickets = json.loads(response.content)
        self.assertEqual(len(tickets), 30)
