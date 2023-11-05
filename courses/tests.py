from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from courses.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@test.ru',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        self.user.set_password('0000')
        self.user.save()
        self.access_token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.course = Course.objects.create(
            title='test_course',
            owner=self.user
        )
        self.course.save()

        self.lesson = Lesson.objects.create(
            title='test_lesson',
            owner=self.user
        )
        self.lesson.save()

        self.subscription = Subscription.objects.create(
            course=self.course
        )
        self.subscription.save()


    def test_create_lesson(self):
        """Тестирование создания урока"""
        data = {'title': 'test', 'course': self.course.pk}
        response = self.client.post('/lessons/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['title'], data['title'])
        self.assertEqual(response.json()['course'], self.course.pk)
        self.assertEqual(response.json()['owner'], self.user.pk)
        self.assertEqual(Lesson.objects.filter(id=response.json()['id']).exists(), True)

    def test_list_lessons(self):
        """Тестирование получения списка уроков"""
        lessons = list(Lesson.objects.all())
        response = self.client.get('/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], len(lessons))
        self.assertEqual(response.json()['results'][0]['id'], lessons[0].pk)

    def test_retrieve_lesson(self):
        """Тестирование получения урока"""
        response = self.client.get(f'/lessons/{self.lesson.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], self.lesson.pk)
        self.assertEqual(response.json()['title'], self.lesson.title)
        self.assertEqual(response.json()['preview'], self.lesson.preview)
        self.assertEqual(response.json()['description'], self.lesson.description)
        self.assertEqual(response.json()['video_url'], self.lesson.video_url)
        self.assertEqual(response.json()['course'], self.lesson.course)
        self.assertEqual(response.json()['owner'], self.lesson.owner.pk)

    def test_update_lesson(self):
        """Тестирование изменения урока"""
        valid_data = {
            'title': 'new_test', 'description': 'Какое-то описание', 'video_url': 'https://www.youtube.com/test'
        }
        invalid_video_url = {'title': 'new_test', 'video_url': 'https://www.test'}
        invalid_description = {'title': 'new_test', 'description': 'Какое-то описание https://www.test'}
        valid_description = {'title': 'new_test', 'description': 'Какое-то описание https://www.youtube.com/test'}
        no_data = {}

        response = self.client.put(f'/lessons/{self.lesson.pk}/update/', valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], valid_data['title'])
        self.assertEqual(response.json()['description'], valid_data['description'])
        self.assertEqual(response.json()['video_url'], valid_data['video_url'])

        response = self.client.put(f'/lessons/{self.lesson.pk}/update/', invalid_video_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Неверный YouTube URL-адрес!']})

        response = self.client.put(f'/lessons/{self.lesson.pk}/update/', invalid_description)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['В описании указан недопустимый URL!']})

        response = self.client.put(f'/lessons/{self.lesson.pk}/update/', valid_description)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(f'/lessons/{self.lesson.pk}/update/', no_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'title': ['Обязательное поле.']})

    def test_delete_lesson(self):
        """Тестирование удаления урока"""
        response = self.client.delete(f'/lessons/{self.lesson.pk}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.filter(pk=self.lesson.pk).exists(), False)

    def test_subscription_create(self):
        """Тестирование создания подписки"""
        data = {'course': self.course.pk}
        response = self.client.post('/subscriptions/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['course'], self.course.pk)
        self.assertEqual(response.json()['user'], self.user.__str__())

        response = self.client.post('/subscriptions/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Подписка уже существует']})

        response = self.client.get(f'/{self.course.pk}/')
        self.assertEqual(response.json()['subscribed'], True)

        self.assertEqual(Subscription.objects.filter(pk=response.json()['id']).exists(), True)

    def test_subscription_delete(self):
        """Тестирование удаления подписки"""
        response = self.client.delete(f'/subscriptions/{self.subscription.pk}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f'/{self.course.pk}/')
        self.assertEqual(response.json()['subscribed'], False)

        self.assertEqual(Subscription.objects.filter(pk=response.json()['id']).exists(), False)
