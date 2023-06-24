from django.urls.base import reverse
from rest_framework.test import APITestCase
from rest_framework import status
# from rest_framework.test import APIRequestFactory


class GenerateTableTestCase(APITestCase):
    def setUp(self):
        self.reversed_url = reverse('generate-table')
        self.data = {
            'table_name': "GTGGGGGG",
            'table_fields': [
                {
                    'field_name': 'first',
                    'field_type': 'number'
                }
            ]
        }

    def tearDown(self):
        pass

    def test_generate_table(self):
        response = self.client.post(self.reversed_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
