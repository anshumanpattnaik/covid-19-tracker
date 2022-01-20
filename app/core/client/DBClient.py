from app.models import Country, CovidStatistics, States


class DBClient:

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def fetch_covid_statistics():
        # countries = Country.objects.all()
        # for country in countries:
        #     try:
        #         states = States.objects.filter(country__states__country=country)
        #         for state in states:
        #             print(state)
        #     except States.DoesNotExist:
        #         pass
        statistics = CovidStatistics.objects.all()
        for statistic in statistics:
            try:
                country = Country.objects.filter(statistics__country__statistics=statistic)
                print(country)
                # print(f'{country.name} ======= {statistic.confirmed}')
            except Country.DoesNotExist:
                pass
        return statistics
