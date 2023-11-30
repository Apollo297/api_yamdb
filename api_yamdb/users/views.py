from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import (
    mixins,
    permissions,
    status,
    viewsets,
)

from api_yamdb.settings import YaMDb_email
from users.models import User
from users.serializers import (
    SignUpSerializer,
    TokenSerializer,
)


class CreateUserViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    '''
    Вьюсет создает объект класса User и отправляет
    на почту код подтверждения.
    '''

    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Successful registration',
            message=f'Токен: {confirmation_code}',
            from_email=YaMDb_email,
            recipient_list=[user.email],
            fail_silently=False
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    '''Вьюсет предоставляет JWT-токен.'''

    queryset = User.objects.all()
    serializer_class = TokenSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
