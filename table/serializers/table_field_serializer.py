from rest_framework import serializers

from table.enums import AllowedFieldTypes


class TableFieldSerializer(serializers.Serializer):
    field_name = serializers.CharField(max_length=255, required=True)
    field_type = serializers.CharField(max_length=20, required=True)

    def validate_field_name(self, field_name):
        if not isinstance(field_name, str):
            raise serializers.ValidationError(
                "Field name must be a string."
            )

        if not len(field_name) > 2:
            raise serializers.ValidationError(
                "Field name must be at least 3 symbols in length."
            )

        return field_name

    def validate_field_type(self, field_type):
        if field_type.upper() not in [e.name for e in AllowedFieldTypes]:
            raise serializers.ValidationError(
                "Field type must be one of the following types: {}.".format(
                    [e.name for e in AllowedFieldTypes])
            )

        return field_type.upper()
