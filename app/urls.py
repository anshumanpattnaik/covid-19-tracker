from django.urls import path

from .admin.views import *
from .views import *

DEV_URL_PATTERN = [
    path('', index),
    path('statistics/<str:date>', GetStatisticsByDate.as_view()),
    path('admin', admin_panel_view),
    path('admin/add-countries', AddCountries.as_view()),
    path('admin/add-statistics', AddStatistics.as_view())
]

PROD_URL_PATTERN = [
    path('', index),
    path('statistics/<str:date>', GetStatisticsByDate.as_view())
]

if bool(int(os.getenv('ADMIN_PANEL_ENABLED'))):
    urlpatterns = DEV_URL_PATTERN
else:
    urlpatterns = PROD_URL_PATTERN
