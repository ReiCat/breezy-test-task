from django.test import TestCase
from rest_framework.test import APIRequestFactory


class AddTableRowsTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def tearDown(self):
        pass
