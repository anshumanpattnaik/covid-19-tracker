from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('csv', parse_csv),
]
