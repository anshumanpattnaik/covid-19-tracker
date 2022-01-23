import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from app.models import CovidStatistics, Country, States


class CovidStatisticsType(DjangoObjectType):
    class Meta:
        model = CovidStatistics
        fields = ('area', 'address', 'confirmed', 'deaths', 'recovered', 'date')
        filter_fields = {
            'date': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)


class CountryType(DjangoObjectType):
    class Meta:
        model = Country
        fields = ('country_code', 'name', 'flag', 'latitude', 'longitude', 'statistics')
        # filter_fields = {
        #     'date': ['exact', 'icontains', 'istartswith']
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
    statistics = graphene.List(CountryType)

    def resolve_statistics(self, info, **kwargs):
        return Country.objects.all()


class GetStatisticsByCountry(graphene.Mutation):
    class Arguments:
        date = graphene.String(required=True)

    statistics = graphene.Field(CovidStatisticsType)

    @classmethod
    def mutate(cls, root, info, date):
        statistics = CovidStatistics.objects.filter(date=date)
        return GetStatisticsByCountry(statistics)


class Mutation(graphene.ObjectType):
    statistics_category = GetStatisticsByCountry.Field()


schema = graphene.Schema(query=Query)
