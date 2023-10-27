from django.urls import path
from rest_framework import routers

from courses.apps import CoursesConfig
from courses.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView

app_name = CoursesConfig.name

router = routers.DefaultRouter()
router.register(r'', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lessons/', LessonListAPIView.as_view(), name='lessons'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson'),
    path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson_delete'),

    path('payments/', PaymentListAPIView.as_view(), name='payments')
] + router.urls
