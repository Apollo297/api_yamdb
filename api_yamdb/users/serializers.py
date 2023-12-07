from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=settings.MAX_LENGTH_EMAIL,
        required=True,
    )
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=settings.MAX_LENGTH_USERNAME,
        required=True,
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя.'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=settings.MAX_LENGTH_USERNAME,
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True
    )


class UserCreatedAdmSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=settings.MAX_LENGTH_USERNAME,
        validators=[
            UniqueValidator(
                queryset=User.objects.all()
            )
        ],
        required=True,
    )
    email = serializers.EmailField(
        max_length=settings.MAX_LENGTH_EMAIL,
        validators=[
            UniqueValidator(
                queryset=User.objects.all()
            )
        ],
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
