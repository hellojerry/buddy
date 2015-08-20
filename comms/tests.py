from django.test import TestCase
from pprint import pprint

class CallDataTest(TestCase):
    
    def test_xml_returned(self):
        response = self.client.get('/api/calls/call_data/')
        self.assertEqual(response._headers['content-type'], ('Content-Type', 'text/xml'))
