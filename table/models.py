from django.contrib import admin
from django.db import models

from table.enums import AllowedFieldTypes


class TableName(models.Model):
    table_name = models.CharField(max_length=255, unique=True)


def create_field(field_name, field_type):
    field = None
    if field_type.upper() == AllowedFieldTypes.STRING.name or field_type == 'character varying':
        field = models.CharField(max_length=255)
    elif (
        field_type.upper() == AllowedFieldTypes.NUMBER.name or
        field_type == 'bigint' or
        field_type == 'integer'
    ):
        field = models.IntegerField(null=True)
    elif field_type.upper() == AllowedFieldTypes.BOOLEAN.name or field_type == 'boolean':
        field = models.BooleanField(default=False)
    field.column = field_name
    field.many_to_many = None
    return field


def create_model(name, fields=None, app_label='', module='', options=None, admin_opts=None):
    """
    Create specified model
    """
    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during model creation
        pass

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': module, 'Meta': Meta}

    # Add in any fields that were provided
    if fields:
        for field in fields:
            field_name = field['field_name']
            field_type = field['field_type']

            attrs[field_name] = create_field(field_name, field_type)

    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (models.Model,), attrs)

    # Create an Admin class if admin options were provided
    if admin_opts is not None:
        class Admin(admin.ModelAdmin):
            pass
        for key, value in admin_opts:
            setattr(Admin, key, value)
        admin.site.register(model, Admin)

    return model
