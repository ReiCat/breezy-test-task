import ujson
from django.db import connection
from django.test import TestCase
from django.urls.base import reverse
from rest_framework import status

from table.models import TableName
from table.utils import create_model


class UpdateTableStructureTestCase(TestCase):
    def test_update_table_structure_returns_error_in_case_of_empty_request_data(self):
        # Arrange
        reversed_url = reverse('update-table-structure', kwargs={
            'table_id': 1
        })

        data = {}

        # Act
        response = self.client.put(
            reversed_url, 
            data, 
            content_type="application/json"
        )
        response_content = ujson.decode(response.content)

        # Assert
        self.assertEqual(response_content['new_table_fields'][0], 'This field is required.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_table_structure_returns_error_in_case_if_new_table_fields_list_is_empty(self):
        # Arrange
        reversed_url = reverse('update-table-structure', kwargs={
            'table_id': 1
        })
         
        data = {
            'new_table_fields': []
        }

        # Act
        response = self.client.put(
            reversed_url, 
            data, 
            content_type="application/json"
        )
        response_content = ujson.decode(response.content)

        # Assert
        self.assertEqual(response_content['new_table_fields'][0], 'Table should have at least one field.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_table_structure_returns_error_in_case_if_table_name_not_found(self):
        # Arrange
        reversed_url = reverse('update-table-structure', kwargs={
            'table_id': 1
        })
         
        data = {
            'new_table_fields': [
                {
                    'field_name': 'qqq',
                    'field_type': 'string'
                }
            ]
        }

        # Act
        response = self.client.put(
            reversed_url, 
            data, 
            content_type="application/json"
        )
        response_content = ujson.decode(response.content)

        # Assert
        self.assertEqual(response_content['detail'], 'Table name not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_table_structure_returns_error_in_case_if_table_not_found(self):
        # Arrange
        table_name = "test_table_name"
        tableObj = TableName.objects.create(table_name=table_name)
        self.assertIsNotNone(tableObj)
        self.assertEqual(tableObj.table_name, table_name)
        self.assertTrue(tableObj.pk > 0)

        reversed_url = reverse('update-table-structure', kwargs={
            'table_id': tableObj.pk
        })

        data = {
            'new_table_fields': [
                {
                    'field_name': 'qqq',
                    'field_type': 'string'
                }
            ]
        }

        # Act
        response = self.client.put(
            reversed_url, 
            data, 
            content_type="application/json"
        )
        response_content = ujson.decode(response.content)

        # Assert
        self.assertEqual(response_content['detail'], 'Table not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_table_structure_returns_response_in_case_of_success(self):
        # Arrange
        data = {
            'table_name': "ddd",
            'table_fields': [
                {
                    'field_name': 'first',
                    'field_type': 'number'
                }
            ]
        }

        tableObj = TableName.objects.create(table_name=data['table_name'])
        self.assertIsNotNone(tableObj)
        self.assertEqual(tableObj.table_name, data['table_name'])
        self.assertTrue(tableObj.pk > 0)

        reversed_url = reverse('update-table-structure', kwargs={
            'table_id': tableObj.pk
        })

        new_model = create_model(
            data['table_name'],
            fields=data['table_fields'],
            app_label='table',
            module='table.models'
        )

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(new_model)

        update_data = {
            'new_table_fields': [
                {
                    'field_name': 'qqq',
                    'field_type': 'string'
                }
            ]
        }

        # Act
        response = self.client.put(
            reversed_url, 
            update_data, 
            content_type="application/json"
        )
        response_content = ujson.decode(response.content)

        # Assert
        self.assertEqual(response_content['table_name'], data['table_name'])
        self.assertEqual(
            response_content['table_fields'][0]['field_name'], 
            update_data['new_table_fields'][0]['field_name']
        )
        self.assertEqual(
            response_content['table_fields'][0]['field_type'], 
            update_data['new_table_fields'][0]['field_type'].upper()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)