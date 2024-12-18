from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('robots.urls')),
    path('', include('orders.urls')),
]
