from django.urls.base import reverse
from rest_framework.test import APITestCase
from rest_framework import status
# from rest_framework.test import APIRequestFactory


class GenerateTableTestCase(APITestCase):
    def setUp(self):
        # self.factory = APIRequestFactory()
        self.reversed_url = reverse('generate-table')
        self.data = {
            'table_name': "GTGGGGGG",
            'table_fields': [
                {
                    'field_name': 'sukka',
                    'field_type': 'number'
                }
            ]
        }

    def tearDown(self):
        pass

    def test_generate_table(self):
        response = self.client.post(self.reversed_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # request = self.factory.post(
        #     'api/table',
        #     {'title': 'new idea'},
        #     format='json'
        # )
        # print("QQQQ test_generate_table", request)
        # self.assertEqual(5, 1)

    # def test_generate_table_returns_shit(self):
    #     request = self.factory.post(
    #         'api/table',
    #         {'title': 'new idea'},
    #         format='json'
    #     )
    #     print("FGFF test_generate_table_returns_shit", request)
    #     self.assertEqual(2, 3)
