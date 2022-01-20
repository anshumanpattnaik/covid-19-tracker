from app.core.JSONEntity import JSONEntity


class Statistics(JSONEntity):
    def __init__(self, area: str = None, confirmed: int = None, deaths: int = None, recovered: int = None,
                 date: str = None):
        self.area = area
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered
        self.date = date


class Country(JSONEntity):
    def __init__(self, name: str = None, flag: str = None, statistics: [Statistics] = None):
        self.name = name
        self.flag = flag
        self.statistics = Statistics.object(statistics)


class CountryNode(JSONEntity):
    def __init__(self, node: Country = None):
        self.node = Country.object(node)


class CountryEdges(JSONEntity):
    def __init__(self, edges: [CountryNode] = None):
        self.edges = CountryNode.object(edges)


class StatisticsNode(JSONEntity):
    def __init__(self, statistics: CountryEdges = None):
        self.statistics = CountryEdges.object(statistics)


class StatisticsData(JSONEntity):
    def __init__(self, data: StatisticsNode = None):
        self.data = StatisticsNode.object(data)
