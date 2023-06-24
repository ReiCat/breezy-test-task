from django.core.cache import cache
from collections import defaultdict
from django.db import connection, models
from django.db.utils import ProgrammingError, IntegrityError
from django.core import serializers as dj_serializers

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import exceptions
from table.serializers.generate_table_serializer import GenerateTableSerializer
from table.serializers.update_table_structure_serializer import UpdateTableStructureSerializer
from table.models import TableName, create_model, create_field, get_table_fields


@api_view(['POST'])
def generate_table(request):
    """Generates dynamic Django model based on user provided fields types and titles."""

    serializer = GenerateTableSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
        return

    table_name = serializer.data['table_name']
    table_fields = serializer.data['table_fields']

    new_model = create_model(
        table_name,
        fields=table_fields,
        app_label='table',
        module='table.models'
    )

    try:
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(new_model)
    except ProgrammingError:
        raise serializers.ValidationError(
            "Table {} is already exists".format(table_name)
        )

    try:
        table = TableName.objects.create(table_name=table_name)
    except IntegrityError:
        # We're passing here because the table has been created but table name already in the db
        pass

    return Response({
        "table_id": table.pk
    }, status=201)


@api_view(['PUT'])
def update_table_structure(request, table_id: int):
    """This end point allows the user to update the structure of dynamically generated model."""

    try:
        table_id = int(table_id)
    except ValueError:
        raise serializers.ValidationError(
            'Wrong table ID specified'
        )

    serializer = UpdateTableStructureSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
        return

    new_table_fields = serializer.data['new_table_fields']
    new_table_field_names = set(map(
        lambda field: field['field_name'], new_table_fields
    ))

    try:
        tableObject = TableName.objects.get(pk=table_id)
    except TableName.DoesNotExist:
        raise exceptions.NotFound

    result = get_table_fields(tableObject.table_name)
    if not result:
        raise exceptions.NotFound

    old_table_fields, old_table_field_names = [], set()
    for field_name, field_type in result:
        if field_name == 'id':
            continue

        old_table_fields.append({
            "field_name": field_name,
            "field_type": field_type
        })
        old_table_field_names.add(field_name)

    old_model = create_model(
        tableObject.table_name,
        fields=old_table_fields,
        # app_label='table',
        module='table.models'
    )

    # Lets exclude fields that are not presented in new_table_field_names
    fields_to_remove = old_table_field_names.difference(new_table_field_names)

    for old_table_field in old_table_fields:
        if old_table_field['field_name'] not in fields_to_remove:
            continue

        field = create_field(
            old_table_field['field_name'],
            old_table_field['field_type']
        )
        with connection.schema_editor() as schema_editor:
            schema_editor.remove_field(
                old_model,
                field
            )

    for new_table_field in new_table_fields:
        field = create_field(
            new_table_field['field_name'],
            new_table_field['field_type']
        )

        try:
            with connection.schema_editor() as schema_editor:
                schema_editor.add_field(
                    old_model,
                    field
                )
        except ProgrammingError:
            # Ignore if the field is already exists
            pass

    return Response({
        "table_name": tableObject.table_name,
        "table_fields": new_table_fields
    }, status=200)


@api_view(['POST'])
def add_table_rows(request, table_id: int):
    """Allows the user to add rows to the dynamically generated model while respecting the model schema."""
    print("ADD TABLE {0}".format(table_id))
    return Response(status=201)


@api_view(['GET'])
def get_table_rows(request, table_id: int):
    """Gets all the rows in the dynamically generated model."""
    try:
        tableObject = TableName.objects.get(pk=table_id)
    except TableName.DoesNotExist:
        raise exceptions.NotFound

    result = get_table_fields(tableObject.table_name)
    if not result:
        raise exceptions.NotFound

    table_fields = []
    for field_name, field_type in result:
        if field_name == 'id':
            continue

        table_fields.append({
            "field_name": field_name,
            "field_type": field_type
        })

    model = create_model(
        tableObject.table_name,
        fields=table_fields,
        app_label='table',
        module='table.models'
    )

    table_rows = model.objects.all()

    return Response(dj_serializers.serialize('json', table_rows), status=200)
