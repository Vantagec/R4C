from django.urls import path

from .views import add_robot, download_production_list


urlpatterns = [
    path(
        'add_robot/', add_robot, name='add_robot'
    ),
    path(
        'download/', download_production_list, name='download_production_list'
    ),
]
