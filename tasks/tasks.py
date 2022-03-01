from cProfile import run
from configparser import SectionProxy
import datetime
import email
import time

from django.contrib.auth.models import User
from django.core.mail import send_mail
from tasks.models import Report, Task
from datetime import timedelta

from celery.decorators import periodic_task

from task_manager.celery import app


@periodic_task(run_every=timedelta(seconds=10))
def send_mail_reminder():
    reports = Report.objects.all()
    for report in reports:
        report_time = report.report_time
        now_time = datetime.datetime.now().time()
        delta_report_time = datetime.timedelta(
            hours=report_time.hour,
            minutes=report_time.minute,
            seconds=report_time.second,
        )
        delta_now_time = datetime.timedelta(
            hours=now_time.hour, minutes=now_time.minute, seconds=now_time.second
        )
        difference = delta_report_time - delta_now_time
        difference_seconds = difference.total_seconds()
        print(f"{difference.total_seconds()} {delta_now_time}  {delta_report_time}")
        if difference_seconds <= 10 and difference_seconds > 0:
            report_user = User.objects.filter(user=report.user)[0]
            pending_qs = Task.objects.filter(
                user=report_user, completed=False, deleted=False
            )
            email_context = f"You have {pending_qs.count()} Pending tasks"
            send_mail(
                "Pendning Task from Task Manager",
                email_context,
                "wolverine@wolverine.com",
                [report_user.email],
            )
    # print("Starting process Emails")
    # for user in User.objects.all():
    #     pending_qs = Task.objects.filter(user=user, completed=False, deleted=False)
    #     email_context = f"You have {pending_qs.count()} Pending tasks"
    # send_mail(
    #     "Pendning Task from Task Manager",
    #     email_context,
    #     "wolverine@wolverine.com",
    #     [user.email],
    # )


# @app.task
# def test_background_jobs():
#     print("This is from bg")
#     for i in range(10):
#         time.sleep(1)
#         print(i)


# @app.task
# def cool_down():
#     time.sleep(3600 * 2)
