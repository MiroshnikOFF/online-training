from rest_framework import serializers

from courses.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Подробный сериализатор пользователя (для владельца профиля или для персонала)"""

    # Список всех платежей пользователя
    payments = PaymentSerializer(source='payment.all', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['pk', 'email', 'password', 'last_name', 'first_name', 'phone', 'city', 'avatar', 'payments']

    def create(self, validated_data):
        """Создает пользователя и устанавливает ему пароль"""

        instance = super().create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        """Обновляет пользователя входящими данными"""

        instance = super().update(instance, validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserSerializerForStranger(serializers.ModelSerializer):
    """Сокращенный сериализатор пользователя (для пользователя не владеющего этим профилем)"""

    class Meta:
        model = User
        fields = ['pk', 'email', 'first_name', 'phone', 'city', 'avatar']
        
