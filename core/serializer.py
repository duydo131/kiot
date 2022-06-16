from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    """BaseSerializer"""

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class IntegerArrayField(serializers.CharField):
    def to_internal_value(self, data):
        super().to_internal_value(data)
        list_not_digit = [x.strip() for x in data.split(',') if not x.strip().isdigit()]
        if list_not_digit:
            raise ValueError(f"{','.join(list_not_digit)} is not a number(NaN)")
        return [int(x.strip()) for x in data.split(',') if x.strip().isdigit()]