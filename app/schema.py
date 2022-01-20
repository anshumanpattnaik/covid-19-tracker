import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from app.models import CovidStatistics, Country, States


class CovidStatisticsType(DjangoObjectType):
    class Meta:
        model = CovidStatistics
        fields = ('area', 'address', 'confirmed', 'deaths', 'recovered', 'date')


class CountryType(DjangoObjectType):
    class Meta:
        model = Country
        fields = ('country_code', 'name', 'flag', 'latitude', 'longitude', 'statistics')
        # filter_fields = {
        #     'country_code': ['exact', 'icontains', 'istartswith']
        # }
        # interfaces = (relay.Node,)


# class StateType(DjangoObjectType):
#     class Meta:
#         model = States
#         fields = ('country', 'name', 'latitude', 'longitude', 'statistics')
#         filter_fields = {
#             'name': ['exact', 'icontains', 'istartswith']
#         }
#         interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    # statistics = DjangoFilterConnectionField(CountryType)
    # states = DjangoFilterConnectionField(StateType)
    countries = graphene.List(CountryType)

    def resolve_countries(self, info, **kwargs):
        return Country.objects.all()


schema = graphene.Schema(query=Query)
