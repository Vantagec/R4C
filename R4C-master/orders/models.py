from django.db import models

from customers.models import Customer


class Order(models.Model):
    """Модель представления заказа на робота"""
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name='Покупатель'
    )
    robot_serial = models.CharField(
        max_length=5,
        blank=False,
        null=False,
        verbose_name='Серийный номер робота'
    )
    is_notified = models.BooleanField(
        default=False,
        verbose_name='Уведомление выслано'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'customer': self.customer.email,
            'robot_serial': self.robot_serial
        }

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['customer', 'robot_serial'],
                name='unique order'
            )
        ]
