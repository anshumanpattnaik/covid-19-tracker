from django.urls import path, re_path
from graphene_django.views import GraphQLView

from .schema import schema
from .views import *

urlpatterns = [
    re_path('graphql', GraphQLView.as_view(graphiql=True, schema=schema)),
    path('', index),
    path('csv', parse_csv),
]
