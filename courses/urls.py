from django.urls import path
from rest_framework import routers

from courses.apps import CoursesConfig
from courses.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView, SubscriptionCreateAPIView, SubscriptionListAPIView, \
    SubscriptionRetrieveAPIView, SubscriptionUpdateAPIView, SubscriptionDestroyAPIView

app_name = CoursesConfig.name

router = routers.DefaultRouter()
router.register(r'', CourseViewSet, basename='courses')

urlpatterns = [
                  path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
                  path('lessons/', LessonListAPIView.as_view(), name='lessons'),
                  path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson'),
                  path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson_update'),
                  path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson_delete'),

                  path('subscriptions/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
                  path('subscriptions/', SubscriptionListAPIView.as_view(), name='subscriptions'),
                  path('subscriptions/<int:pk>/', SubscriptionRetrieveAPIView.as_view(), name='subscription'),
                  path('subscriptions/<int:pk>/update/', SubscriptionUpdateAPIView.as_view(),
                       name='subscriptions_update'),
                  path('subscriptions/<int:pk>/delete/', SubscriptionDestroyAPIView.as_view(),
                       name='subscriptions_delete'),

                  path('payments/', PaymentListAPIView.as_view(), name='payments'),
              ] + router.urls
