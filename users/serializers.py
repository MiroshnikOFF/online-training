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

        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """Обновляет пользователя входящими данными"""

        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.city = validated_data.get('city', instance.city)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance


class UserSerializerForStranger(serializers.ModelSerializer):
    """Сокращенный сериализатор пользователя (для пользователя не владеющего этим профилем)"""

    class Meta:
        model = User
        fields = ['pk', 'email', 'first_name', 'phone', 'city', 'avatar']
        
