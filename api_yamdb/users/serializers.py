from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True,
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя.'
            )
        return value

    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserCreatedAdmSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        validators=[
            UniqueValidator(
                queryset=User.objects.all()
            )
        ],
        required=True,
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[
            UniqueValidator(
                queryset=User.objects.all()
            )
        ],
        required=True,
    )
    first_name = serializers.CharField(
        max_length=150,
        required=False
    )
    last_name = serializers.CharField(
        max_length=150,
        required=False
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
