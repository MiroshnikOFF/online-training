from datetime import datetime, timedelta

from django.core.mail import send_mail
from celery import shared_task

from config import settings
from users.models import User


@shared_task
def send_notification_task(course_title, recipient_list):
    """
    Рассылает письма пользователям об обновлении материалов курса при активной подписке.
    """
    send_mail(
        subject=f'Обновления в курсе {course_title}!',
        message=f'В курсе {course_title} произошли обновления, посетите наш сайт.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list
    )


@shared_task
def check_user_last_login_task():
    """
    Периодическая задача. Проверяет пользователей по дате последнего входа по паролю
    и если пользователь не заходил более месяца, блокирует его.
    """
    for user in User.objects.all():
        if user.last_login:
            delta = datetime.now() - user.last_login.replace(tzinfo=None)
            if delta > timedelta(days=30):
                user.is_active = False
                user.save()
