from rest_framework import serializers


class FieldsValidator:
    error_message = "Field list should not be empty"

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, attrs):
        print("ATTRS SUYKKA", attrs)
        # if len(self.fields) == 0:
        #     raise serializers.ValidationError(
        #         self.error_message,
        #         code='date_before'
        #     )
