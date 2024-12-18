import os
from datetime import timedelta, date

import xlsxwriter
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models.query import QuerySet


def create_production_list(robots: QuerySet) -> str:
    """
    Функция для создания xlsx файла со сводной
    информацией о произведенных роботах.
    """
    dict_robots = {}
    for robot in robots:
        dict_robots[robot['model__name']] = dict_robots.get(
            robot['model__name'], []
        ) + [robot]

    workbook = xlsxwriter.Workbook('production_list/robots_list.xlsx')
    workbook.set_properties({'encoding': 'utf-8'})
    for model, list_models in dict_robots.items():
        worksheet = workbook.add_worksheet(name=model)
        worksheet.write(0, 0, 'Модель')
        worksheet.write(0, 1, 'Версия')
        worksheet.write(0, 2, 'Количество за неделю')
        for ind, robot in enumerate(list_models):
            worksheet.write(ind+1, 0, robot['model__name'])
            worksheet.write(ind+1, 1, robot['version__name'])
            worksheet.write(ind+1, 2, robot['robot_count'])
    workbook.close()

    return os.path.join(settings.BASE_DIR, 'production_list/robots_list.xlsx')


def get_difference_datetime_from_today(days: int) -> date:
    """Функция для получения даты <days> дней назад."""
    start_date = timezone.now().date() - timedelta(days=days)
    return start_date


def notify_customers(
        emails: list[str], robot_model: str, robot_version: str
) -> None:
    """
    Функция для отправки email списку получателей.

    Должны быть определены переменные в файле settings.py:
    - EMAIL_HOST
    - EMAIL_PORT
    - EMAIL_USE_SSL
    - EMAIL_HOST_USER
    - EMAIL_HOST_PASSWORD
    """
    message = f"""
    Добрый день!
    Недавно вы интересовались нашим роботом модели {robot_model}, версии {robot_version}.
    Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами
    """
    send_mail(
        subject='Робот в наличии!',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=emails,
        fail_silently=False
    )
