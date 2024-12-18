from django.db import models


class Customer(models.Model):
    """Модель представления покупателя"""
    email = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name='Email покупателя'
    )
