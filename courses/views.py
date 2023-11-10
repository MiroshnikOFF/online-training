from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from courses.models import Course, Lesson, Payment, Subscription
from courses.pagination import CoursesLessonsPaginator
from courses.permissions import IsNotModeratorForViewSet, IsOwner, IsNotModeratorForAPIView
from courses.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from courses.services import send_notification
from courses.stripe import create_intent, get_intent


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsNotModeratorForViewSet,)
    serializer_class = CourseSerializer
    pagination_class = CoursesLessonsPaginator

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

    def update(self, request, *args, **kwargs):
        """При обновлении курса высылает уведомление пользователю при активной подписке"""
        course = Course.objects.get(pk=kwargs['pk'])
        send_notification(course)
        return super().update(request, *args, **kwargs)


class LessonCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsNotModeratorForAPIView,)
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        """Сохраняет авторизованного пользователя в объекте урока"""

        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

    def create(self, request, *args, **kwargs):
        if 'course' in request.data:
            course = Course.objects.get(pk=request.data['course'])
            send_notification(course)
        return super().create(request, *args, **kwargs)


class LessonListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LessonSerializer
    pagination_class = CoursesLessonsPaginator

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


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        """Создает намерение платежа с помощью Stripe"""

        super().post(request, *args, **kwargs)
        return create_intent(request)

    def perform_create(self, serializer):
        """Сохраняет авторизованного пользователя и stripe id в объекте платежа"""

        new_payment = serializer.save()
        new_payment.user = self.request.user
        new_payment.stripe_id = create_intent(self.request).data['intent']['id']
        new_payment.save()


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get(self, request, *args, **kwargs):
        """Выводит данные о платеже с помощью Stripe"""

        return get_intent(kwargs['pk'])


class SubscriptionCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        """Сохраняет авторизованного пользователя в объекте подписки"""

        new_subscription = serializer.save()
        new_subscription.user = self.request.user
        new_subscription.subscribed = True
        new_subscription.save()


class SubscriptionListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Subscription.objects.all()
