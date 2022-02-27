from cProfile import run
from configparser import SectionProxy
import email
import time

from django.contrib.auth.models import User
from django.core.mail import send_mail
from tasks.models import Task
from datetime import timedelta

from celery.decorators import periodic_task

from task_manager.celery import app


@periodic_task(run_every=timedelta(seconds=10))
def send_mail_reminder():
    print("Starting process Emails")
    for user in User.objects.all():
        pending_qs = Task.objects.filter(user=user, completed=False, deleted=False)
        email_context = f"You have {pending_qs.count()} Pending tasks"
        send_mail(
            "Pendning Task from Task Manager",
            email_context,
            "wolverine@wolverine.com",
            [user.email],
        )


@app.task
def test_background_jobs():
    print("This is from bg")
    for i in range(10):
        time.sleep(1)
        print(i)


@app.task
def cool_down():
    time.sleep(3600 * 2)
