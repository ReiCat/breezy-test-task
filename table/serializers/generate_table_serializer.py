from rest_framework import serializers

from table.serializers.table_field_serializer import TableFieldSerializer


class GenerateTableSerializer(serializers.Serializer):
    table_name = serializers.CharField(max_length=255, required=True)
    table_fields = TableFieldSerializer(many=True)

    def validate_table_name(self, table_name):
        if not isinstance(table_name, str):
            raise serializers.ValidationError(
                "Table name must be a string"
            )

        if not len(table_name) > 2:
            raise serializers.ValidationError(
                "Table name must be at least 3 symbols in length"
            )

        if (
            table_name == 'table_tablename' or
            table_name.startswith('auth_') or
            table_name.startswith('django_')
        ):
            raise serializers.ValidationError(
                "You cannot use reserved table names, please choose another one"
            )

        return table_name

    def validate_table_fields(self, table_fields):
        if not len(table_fields) > 0:
            raise serializers.ValidationError(
                "Table should have at least one field"
            )

        return table_fields
