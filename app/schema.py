import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from app.models import CovidStatistics, Country, States, TotalCases


class TotalCasesType(DjangoObjectType):
    class Meta:
        model = TotalCases
        fields = ('total_confirmed', 'total_deaths', 'total_recovered', 'date')
        filter_fields = {
            'date': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)


class CovidStatisticsType(DjangoObjectType):
    class Meta:
        model = CovidStatistics
        fields = ('area', 'confirmed', 'deaths', 'recovered', 'date')
        filter_fields = {
            'date': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)


class CountryType(DjangoObjectType):
    class Meta:
        model = Country
        fields = ('code', 'name', 'flag', 'coordinates', 'statistics')


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
    total_cases = DjangoFilterConnectionField(TotalCasesType)
    statistics = graphene.List(CountryType)

    def resolve_total_cases(self, info, **kwargs):
        return TotalCases.objects.all()

    def resolve_statistics(self, info, **kwargs):
        return Country.objects.all()


schema = graphene.Schema(query=Query)
