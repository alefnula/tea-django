from rest_framework import serializers
from tea_django.consts import COLOR_RE
from rest_framework.exceptions import ValidationError


def color_validator(value):
    if COLOR_RE.match(value) is None:
        raise ValidationError(f"Invalid color string: {value}")
    return value


class ColoredCreateSerializer(serializers.Serializer):
    color = serializers.CharField(max_length=7, validators=[color_validator])


class ColoredUpdateSerializer(serializers.Serializer):
    color = serializers.CharField(
        max_length=7,
        validators=[color_validator],
        required=False,
        allow_null=True,
    )

    def update(self, instance, validated_data):
        color = validated_data.get("color", None)
        if color is not None:
            instance.color = color
