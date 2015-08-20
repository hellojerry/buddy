from django.test import TestCase

class HomePageTest(TestCase):
    
    def test_base_template_returned(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'base.html')