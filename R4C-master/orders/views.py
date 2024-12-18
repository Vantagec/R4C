from http import HTTPStatus

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .forms import OrderForm
from .models import Order
from customers.models import Customer


@csrf_exempt
@require_http_methods(['POST'])
def create_order(request):
    """
    Вью функция для создания заказа.

    Если покупателя с полученным email не существует - создаем.
    Создаем/обновляем заказ на соотвествующего робота.
    """
    form = OrderForm(request.POST)
    form_data = form.data
    if form.is_valid():

        # Создаем покупателя
        customer, _ = Customer.objects.get_or_create(
            email=form_data['email']
        )
        # Создаем/обновляем заказ на робота
        order, _ = Order.objects.update_or_create(
            customer=customer,
            robot_serial=form_data['robot_serial'],
            defaults={'is_notified': False}
        )
        return JsonResponse(
            {'data': order.to_dict()},
            status=HTTPStatus.CREATED
        )
    return JsonResponse(
        {'message': 'Не удалось создать заказ'},
        status=HTTPStatus.BAD_REQUEST
    )
