from django.db import models


class TableName(models.Model):
    table_name = models.CharField(max_length=255, unique=True)
