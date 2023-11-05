from django.db import models

from config import settings
from users.models import NULLABLE, User


class Course(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    preview = models.ImageField(upload_to='courses/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='Владелец')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('pk',)


class Lesson(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    preview = models.ImageField(upload_to='courses/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    video_url = models.URLField(verbose_name='Видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, related_name='lesson',
                               verbose_name='Курс')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='Владелец')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('pk',)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, related_name='payment',
                             verbose_name='Пользователь')
    date = models.DateTimeField(auto_now_add=True, **NULLABLE, verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, related_name='payment',
                               verbose_name='Оплаченный курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, **NULLABLE, related_name='payment',
                               verbose_name='Оплаченный урок')
    total_paid = models.IntegerField(verbose_name='Сумма оплаты')
    method = models.CharField(max_length=100, **NULLABLE, verbose_name='Способ оплаты')

    def __str__(self):
        return f"{self.total_paid} от {self.user}"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                             related_name='subscription', verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscription', verbose_name='Курс')
    subscribed = models.BooleanField(default=False, verbose_name='Признак подписки')

    def __str__(self):
        return f"{self.subscribed} - {self.course} - {self.user}"

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('pk',)
