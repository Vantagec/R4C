import os
import json
from http import HTTPStatus

from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.shortcuts import get_object_or_404

from orders.models import Order
from robots.constans import NUMBER_OF_DAYS_TO_UPLOAD_A_FILE
from .validators import validate_robot_data
from .models import Robot, Model, Version
from .utils import create_production_list, get_difference_datetime_from_today, notify_customers


@csrf_exempt
@require_http_methods(['POST'])
def add_robot(request):
    """
    Вью функция для добавления робота.

    Создает робота на основании полученных из запроса данных.
    Если указаны несуществующие модель/версия робота, возвращается 404.
    При успешном добавлении робота, проверяются заказы покупателей на
    данного робота. Если такие заказы есть, заказчикам отправляется
    уведомление на email.
    """

    data = json.loads(request.body)
    if validate_robot_data(data):

        # Создаем робота
        model = get_object_or_404(Model, name=data['model'])
        version = get_object_or_404(Version, name=data['version'], model=model)
        created = data['created']
        robot = Robot.objects.create(
            serial=f'{data["model"]}-{data["version"]}',
            model=model,
            version=version,
            created=created
        )

        # Уведомляем покупателей о наличии
        orders = Order.objects.filter(
            robot_serial=robot.serial, is_notified=False
        )
        if orders:
            customer_emails = [order.customer.email for order in orders]
            notify_customers(
                emails=customer_emails,
                robot_model=robot.model,
                robot_version=robot.version
            )
            orders.update(is_notified=True)

        return JsonResponse(
            {'data': robot.to_dict()},
            status=HTTPStatus.CREATED
        )
    return JsonResponse(
        {'message': 'Полученные данные не соотвествуют ожиданиям'},
        status=HTTPStatus.BAD_REQUEST
    )


@require_http_methods(['GET'])
def download_production_list(request):
    """
    Вью функция для получение ексель файла с информацией о
    произведенных роботах за последние N дней.
    """
    # Получаем сводную информацию о произведенных роботах
    robots = Robot.objects.filter(
        created__date__gte=get_difference_datetime_from_today(
            days=NUMBER_OF_DAYS_TO_UPLOAD_A_FILE
        )
    ).values('model__name', 'version__name').annotate(robot_count=Count('id'))

    # Создаем xlsx файл
    prod_list = create_production_list(robots)

    # Возвращаем файл в ответе
    if os.path.exists(prod_list):
        with open(prod_list, 'rb') as fh:
            response = HttpResponse(
                fh.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=production_list.xlsx'
        return response
    return Http404
