import ujson
from django.db import connection
from django.test import TestCase
from django.urls.base import reverse
from rest_framework import status

from table.models import TableName
from table.utils import create_model


class GetTableRowsTestCase(TestCase):
    def test_get_table_rows_returns_error_in_case_of_table_not_found(self):
        # Arrange
        reversed_url = reverse('get-table-rows', kwargs={
            'table_id': 1
        })

        # Act
        response = self.client.get(reversed_url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_table_rows_returns_error_in_case_of_table_fields_not_found(self):
        # Arrange
        tableObj = TableName.objects.create(table_name="test_table_name")

        self.assertIsNotNone(tableObj)

        reversed_url = reverse('get-table-rows', kwargs={
            'table_id': tableObj.pk
        })

        # Act
        response = self.client.get(reversed_url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_table_rows_returns_table_rows_in_case_of_success(self):
        # Arrange
        data = {
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

        new_model = create_model(
            'aaa',
            fields=data['table_fields'],
            app_label='table',
            module='table.models'
        )

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(new_model)

        tableObj = TableName.objects.create(table_name=data['table_name'])
        self.assertIsNotNone(tableObj)


        add_table_row_reversed_url = reverse('add-table-row', kwargs={
            'table_id': tableObj.pk,
        })

        response = self.client.post(add_table_row_reversed_url, add_table_row_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Act
        get_table_rows_reversed_url = reverse('get-table-rows', kwargs={
            'table_id': tableObj.pk
        })

        response = self.client.get(get_table_rows_reversed_url)
        resp_json = ujson.decode(response.content)

        # Assert
        self.assertEqual(len(resp_json), 1)
        self.assertEqual(resp_json[0]['id'], 1)
        self.assertEqual(resp_json[0]['first'], add_table_row_data['first'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)