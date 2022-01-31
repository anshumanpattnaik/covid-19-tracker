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
        fields = ('name', 'code', 'flag', 'coordinates', 'statistics', 'states')


class StateType(DjangoObjectType):
    class Meta:
        model = States
        fields = ('name', 'coordinate', 'date', 'statistics')
        filter_fields = {
            'date': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    total_cases = DjangoFilterConnectionField(TotalCasesType)
    country_statistics = graphene.List(CountryType)
    # states_statistics = DjangoFilterConnectionField(StateType)

    def resolve_total_cases(self, info, **kwargs):
        return TotalCases.objects.all()

    def resolve_country_statistics(self, info, **kwargs):
        return Country.objects.all()

    # def resolve_states_statistics(self, info, **kwargs):
    #     return States.objects.all()


schema = graphene.Schema(query=Query)
