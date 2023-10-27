from rest_framework import serializers

from courses.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(source='payment.all', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['pk', 'email', 'last_name', 'first_name', 'phone', 'city', 'avatar', 'payments']
