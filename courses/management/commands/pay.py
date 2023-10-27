from django.core.management import BaseCommand

from courses.models import Payment, Lesson, Course
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):

        user = User.objects.get(pk=int(input("Пользователь: ")))

        lesson = None
        course = None
        choice = int(input("Урок - 1, курс - 2: "))
        if choice == 1:
            lesson = Lesson.objects.get(pk=int(input("Урок: ")))
        elif choice == 2:
            course = Course.objects.get(pk=int(input("Курс: ")))

        method = int(input("Наличные - 1, перевод - 2: "))
        if method == 1:
            method = 'cash'
        elif method == 2:
            method = 'transfer'

        total_paid = int(input("Сумма: "))

        Payment.objects.create(user=user, course=course, lesson=lesson, total_paid=total_paid, method=method)

        print('Платеж создан')
