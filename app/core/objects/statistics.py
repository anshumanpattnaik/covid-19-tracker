from typing import List

from app.core.JSONEntity import JSONEntity


class TotalCasesField(JSONEntity):
    def __init__(self, totalConfirmed: int = None, totalDeaths: int = None, totalRecovered: int = None,
                 date: str = None):
        self.totalConfirmed = totalConfirmed
        self.totalDeaths = totalDeaths
        self.totalRecovered = totalRecovered
        self.date = date


class TotalCasesNode(JSONEntity):
    def __init__(self, node: TotalCasesField = None):
        self.node = TotalCasesField.object(node)


class TotalCasesEdges(JSONEntity):
    def __init__(self, edges: [TotalCasesNode] = None):
        self.edges = TotalCasesNode.object(edges)


class Statistics(JSONEntity):
    def __init__(self, area: str = None, confirmed: int = None, deaths: int = None, recovered: int = None,
                 date: str = None):
        self.area = area
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered
        self.date = date


class StatisticsNode(JSONEntity):
    def __init__(self, node: Statistics = None):
        self.node = Statistics.object(node)


class StatisticsEdges(JSONEntity):
    def __init__(self, edges: [StatisticsNode] = None):
        self.edges = StatisticsNode.object(edges)


class States(JSONEntity):
    def __init__(self, name: str = None, coordinate: List = None, statistics: StatisticsEdges = None):
        self.name = name
        self.coordinate = coordinate
        self.statistics = StatisticsEdges.object(statistics)


class Country(JSONEntity):
    def __init__(self, name: str = None, code: str = None, flag: str = None, coordinates: List = None,
                 statistics: StatisticsEdges = None, states: States = None):
        self.name = name
        self.code = code
        self.flag = flag
        self.coordinates = coordinates
        self.statistics = StatisticsEdges.object(statistics)
        self.states = States.object(states)


class CountryStatistics(JSONEntity):
    def __init__(self, totalCases: TotalCasesEdges = None, countryStatistics: [Country] = None):
        self.totalCases = TotalCasesEdges.object(totalCases)
        self.countryStatistics = Country.object(countryStatistics)


class StatisticsData(JSONEntity):
    def __init__(self, data: CountryStatistics = None):
        self.data = CountryStatistics.object(data)
