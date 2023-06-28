import ujson
from django.urls.base import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from table.models import TableName


class AddTableRowTestCase(APITestCase):
    def test_get_table_name_returns_error_in_case_if_not_found(self):
        # Arrange
        self.data = {}
        reversed_url = reverse('add_table_row', kwargs={
            'table_id': 1
        })

        # Act
        response = self.client.post(reversed_url, self.data)
        response_content = ujson.decode(response.content)

        # Assert
        self.assertEqual(
            response_content['detail'], 'Not found.'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_table_fields_returns_error_in_case_if_not_found(self):
        # Arrange
        self.data = {}
        tableObj = TableName.objects.create(table_name="test_table_name")

        self.assertIsNotNone(tableObj)

        reversed_url = reverse('add_table_row', kwargs={
            'table_id': 1
        })

        # Act
        response = self.client.post(reversed_url, self.data)
        response_content = ujson.decode(response.content)

        # Assert
        self.assertEqual(
            response_content['detail'], 'Not found.'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_table_row_in_case_of_success(self):
        # Arrange
        generate_table_data = {
            'table_name': "aaa",
            'table_fields': [
                {
                    'field_name': 'first',
                    'field_type': 'number'
                }
            ]
        }
        add_table_row_data = {
            'first': 321
        }
        generate_table_reversed_url = reverse('generate-table')
        
        response = self.client.post(generate_table_reversed_url, generate_table_data)
        generated_table_response_content = ujson.decode(response.content)
        
        self.assertTrue(generated_table_response_content['table_id'] > 0)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        add_table_row_reversed_url = reverse('add_table_row', kwargs={
            'table_id': generated_table_response_content['table_id'],
        })

        # Act
        response = self.client.post(add_table_row_reversed_url, add_table_row_data)
        add_table_row_response_content = ujson.decode(response.content)

        # Assert
        self.assertEqual(
            add_table_row_response_content['table_id'], 
            generated_table_response_content['table_id']
        )
        self.assertEqual(
            add_table_row_response_content['table_name'], 
            generate_table_data['table_name']
        )
        self.assertTrue(add_table_row_response_content['table_row_id'] > 0)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
