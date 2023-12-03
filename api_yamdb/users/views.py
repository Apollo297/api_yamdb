from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated,)
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import (
    filters,
    mixins,
    permissions,
    status,
    viewsets,
)

from api_yamdb.settings import YaMDb_email
from users.models import User
from users.permissions import AdminPermission
from users.serializers import (
    SignUpSerializer,
    TokenSerializer,
    UserCreatedAdmSerializer,
)


class SignUpUserViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
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
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        try:
            user, create = User.objects.get_or_create(
                username=username,
                email=email
            )
        except IntegrityError:
            return Response(
                'Такое username или email уже существует.',
                status=status.HTTP_400_BAD_REQUEST,
            )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Successful registration',
            message=f'Токен: {confirmation_code}',
            from_email=YaMDb_email,
            recipient_list=(user.email,),
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
            access_token = AccessToken.for_user(user)
            return Response(
                {'token': str(access_token)},
                status=status.HTTP_200_OK
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreatedAdmSerializer
    permission_classes = (
        IsAuthenticated,
        AdminPermission,
    )
    lookup_field = 'username'
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter
    )
    search_fields = ('username',)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    @action(
        detail=False,
        methods=['get', 'patch', 'delete'],
        url_path=r'(?P<username>[\w.@+-]+\Z)',
    )
    def get_user_using_username(self, request, username):
        '''Получить данные учетной записи пользователя по username
        с возможностью изменения.
        '''
        user = get_object_or_404(
            User,
            username=username
        )
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def user_data(self, request):
        '''Получить данные своей учетной записи с возможностью изменения.'''
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True,
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        serializer = self.get_serializer(request.user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
