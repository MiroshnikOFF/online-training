from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.permissions import IsOwnerProfile
from users.serializers import UserSerializer, UserSerializerForStranger


class UserRegister(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_serializer_class(self):
        """Получает подробный сериализатор для персонала и сокращенный для пользователей"""

        if self.request.user.is_staff:
            serializer_class = UserSerializer
        else:
            serializer_class = UserSerializerForStranger
        return serializer_class


class UserRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_serializer_class(self):
        """Получает подробный сериализатор для персонала или владельца профиля, для остальных - сокращенный"""

        if self.kwargs['pk'] == self.request.user.pk or self.request.user.is_staff:
            serializer_class = UserSerializer
        else:
            serializer_class = UserSerializerForStranger
        return serializer_class


class UserUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsOwnerProfile)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDestroyAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwnerProfile,)
    queryset = User.objects.all()
    serializer_class = UserSerializer





