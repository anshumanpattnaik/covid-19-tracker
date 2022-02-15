class Utils:

    @staticmethod
    def graphql_query(date):
        return '{ totalCases(date:' + '"' + str(date) + '"' + ') { edges { node { totalConfirmed totalDeaths ' \
                                                              'totalRecovered date } } } countryStatistics { name code ' \
                                                              'flag coordinates statistics(date: ' + '"' + str(date) \
               + '"' + ') { edges { node { area confirmed deaths recovered } } } } }'
