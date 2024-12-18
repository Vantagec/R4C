from django.db import models


class Model(models.Model):
    """Модель представления модели робота"""
    name = models.CharField(
        max_length=2,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Название модели'
    )

    def __str__(self) -> str:
        return self.name


class Version(models.Model):
    """Модель представления версии модели робота"""
    name = models.CharField(
        max_length=2,
        blank=False,
        null=False,
        verbose_name='Название версии'
    )
    model = models.ForeignKey(
        Model,
        on_delete=models.CASCADE,
        verbose_name='Модель'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'model'],
                name='unique model_version'
            )
        ]


class Robot(models.Model):
    """Модель представления робота"""
    serial = models.CharField(
        max_length=5,
        blank=False,
        null=False,
        verbose_name='Серийный номер'
    )
    model = models.ForeignKey(
        Model,
        on_delete=models.CASCADE,
        verbose_name='Модель'
    )
    version = models.ForeignKey(
        Version,
        on_delete=models.CASCADE,
        verbose_name='Версия'
    )
    created = models.DateTimeField(
        blank=False,
        null=False,
        verbose_name='Дата создания'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'serial': self.serial,
            'model': str(self.model),
            'version': str(self.version),
            'created': self.created,
        }
