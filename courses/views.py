from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from courses.models import Course, Lesson, Payment
from courses.permissions import IsNotModeratorForViewSet, IsOwner, IsNotModeratorForAPIView
from courses.serializers import CourseSerializer, LessonSerializer, PaymentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsNotModeratorForViewSet,)
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        """Сохраняет авторизованного пользователя в объекте курса"""

        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_queryset(self):
        """Получает курсы авторизованного пользователя или все курсы для персонала"""

        user = self.request.user
        if user.is_staff:
            return Course.objects.all()
        return Course.objects.filter(owner=user.pk)


class LessonCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsNotModeratorForAPIView,)
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        """Сохраняет авторизованного пользователя в объекте урока"""

        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LessonSerializer

    def get_queryset(self):
        """Получает уроки авторизованного пользователя или все уроки для персонала"""

        user = self.request.user
        if user.is_staff:
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user.pk)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsOwner,)
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsOwner,)
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsNotModeratorForAPIView, IsOwner,)
    queryset = Lesson.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ('date',)
    filterset_fields = ('course', 'lesson', 'method',)

