from django_celery_beat.models import PeriodicTask, IntervalSchedule


def set_schedule(*args, **kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.SECONDS,
        )
    PeriodicTask.objects.create(
        interval=schedule,
        name='Check user last login',
        task='courses.tasks.check_user_last_login_task',
    )