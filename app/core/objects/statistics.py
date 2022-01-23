from app.core.JSONEntity import JSONEntity


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


class Country(JSONEntity):
    def __init__(self, name: str = None, flag: str = None, latitude: float = None, longitude: float = None,
                 statistics: StatisticsEdges = None):
        self.name = name
        self.flag = flag
        self.latitude = latitude
        self.longitude = longitude
        self.statistics = StatisticsEdges.object(statistics)


class CountryStatistics(JSONEntity):
    def __init__(self, statistics: [Country] = None):
        self.statistics = Country.object(statistics)


class StatisticsData(JSONEntity):
    def __init__(self, data: CountryStatistics = None):
        self.data = CountryStatistics.object(data)
