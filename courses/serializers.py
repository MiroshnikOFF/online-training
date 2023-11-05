from rest_framework import serializers

from courses.models import Course, Lesson, Payment, Subscription
from courses.validators import DescriptionValidator, VideoUrlValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            DescriptionValidator(fields='description'),
            VideoUrlValidator(fields='video_url')
        ]


class CourseSerializer(serializers.ModelSerializer):
    # Количество уроков в курсе
    lessons_count = serializers.IntegerField(source='lesson.all.count', read_only=True)

    # Список всех уроков курса
    lessons = LessonSerializer(source='lesson.all', many=True, read_only=True)

    # Признак подписки на курс
    subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        validators = [
            DescriptionValidator(fields='description'),
        ]

    def get_subscribed(self, obj):
        """Проверяет наличие подписки в базе и возвращает результат в поле subscribed"""

        user = self.context['request'].user
        if Subscription.objects.filter(user=user).filter(course=obj).exists():
            return True
        return False


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    subscribed = serializers.BooleanField(read_only=True)
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'

    def validate(self, attrs):
        """Если такая подписка уже существует, то вызывает ошибку валидации"""

        user = self.context['request'].user
        course = Course.objects.get(pk=attrs['course'].pk)
        if Subscription.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError("Подписка уже существует")
        return attrs

