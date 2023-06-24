from rest_framework import serializers

from table.serializers.table_field_serializer import TableFieldSerializer


class UpdateTableStructureSerializer(serializers.Serializer):
    new_table_fields = TableFieldSerializer(many=True)

    def validate_new_table_fields(self, new_table_fields):
        if not len(new_table_fields) > 0:
            raise serializers.ValidationError(
                "Table should have at least one field"
            )

        return new_table_fields
