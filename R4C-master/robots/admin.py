from django.contrib import admin
from .models import Model, Version


@admin.register(Model)
class RobotModelAdmin(admin.ModelAdmin):
    list_display = ['name',]
    pass


@admin.register(Version)
class RobotVersionAdmin(admin.ModelAdmin):
    list_display = ['name', 'model']
    pass
