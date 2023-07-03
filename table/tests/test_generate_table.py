import ujson
from django.urls.base import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# from rest_framework.test import APIRequestFactory


class GenerateTableTestCase(APITestCase):
    def setUp(self):
        self.reversed_url = reverse('generate-table')

    def test_generate_table_returns_error_in_case_of_empty_request_data(self):
        # Arrange
        self.data = {}

        # Act
        response = self.client.post(self.reversed_url, self.data)
        response_content = ujson.decode(response.content)

        # Assert
        self.assertEqual(response_content['table_name'][0], 'This field is required.')
        self.assertEqual(response_content['table_fields'][0], 'This field is required.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_table_returns_error_in_case_of_empty_field_values_provided(self):
        # Arrange
        self.data = {
            'table_name': "",
            'table_fields': []
        }

        # Act
        response = self.client.post(self.reversed_url, self.data)
        response_content = ujson.decode(response.content)

        # Assert
        self.assertEqual(response_content['table_name'][0], 'This field may not be blank.')
        self.assertEqual(response_content['table_fields'][0], 'Table should have at least one field.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_table_returns_error_in_case_of_table_name_is_less_than_three_symbols_in_length(self):
        # Arrange
        self.data = {
            'table_name': "aa",
            'table_fields': [
                {
                    'field_name': 'first',
                    'field_type': 'number'
                }
            ]
        }

        # Act
        response = self.client.post(self.reversed_url, self.data)
        response_content = ujson.decode(response.content)

        # Assert
        self.assertEqual(response_content['table_name'][0], 'Table name must be at least 3 symbols in length.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_table_returns_error_in_case_of_table_has_zero_fields(self):
        # Arrange
        self.data = {
            'table_name': "aaa",
            'table_fields': []
        }

        # Act
        response = self.client.post(self.reversed_url, self.data)
        response_content = ujson.decode(response.content)

        # Assert
        self.assertEqual(response_content['table_fields'][0], 'Table should have at least one field.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_table_returns_error_in_case_if_field_name_is_less_than_three_symbols_in_length(self):
        # Arrange
        self.data = {
            'table_name': "aaa",
            'table_fields': [
                {
                    'field_name': 'fi',
                    'field_type': 'number'
                }
            ]
        }

        # Act
        response = self.client.post(self.reversed_url, self.data)
        response_content = ujson.decode(response.content)

        # Assert
        self.assertEqual(
            response_content['table_fields'][0]['field_name'][0], 
            'Field name must be at least 3 symbols in length'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_table_returns_error_in_case_if_field_type_is_wrong(self):
        # Arrange
        self.data = {
            'table_name': "aaa",
            'table_fields': [
                {
                    'field_name': 'field',
                    'field_type': 'ewq'
                }
            ]
        }

        # Act
        response = self.client.post(self.reversed_url, self.data)
        response_content = ujson.decode(response.content)

        # Assert
        self.assertEqual(
            response_content['table_fields'][0]['field_type'][0], 
            "Field type must be one of the following types: ['STRING', 'NUMBER', 'BOOLEAN']"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_table_returns_error_in_case_of_table_is_already_exists(self):
        # Arrange
        self.data = {
            'table_name': "aaa",
            'table_fields': [
                {
                    'field_name': 'first',
                    'field_type': 'number'
                }
            ]
        }

        # Act
        self.client.post(self.reversed_url, self.data)

        # Making the same request second time
        response = self.client.post(self.reversed_url, self.data)
        response_content = ujson.decode(response.content)

        # Assert
        self.assertEqual(
            response_content[0], 
            "Table {} is already exists".format(self.data['table_name'])
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_table_returns_table_id_in_case_of_success(self):
        # Arrange
        self.data = {
            'table_name': "aaa",
            'table_fields': [
                {
                    'field_name': 'first',
                    'field_type': 'number'
                }
            ]
        }

        # Act
        response = self.client.post(self.reversed_url, self.data)
        response_content = ujson.decode(response.content)


        # Assert
        self.assertTrue(response_content['table_id'] > 0)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)