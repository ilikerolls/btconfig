from __future__ import division, absolute_import, print_function

from btconfig import BTConfigApiClient


class CoinGeckoClient(BTConfigApiClient):

    '''
    CoinGecko Client

    API rate limit of 100 calls per minute - if
    you exceed that limit you will be blocked
    until the next 1 minute window. Do revise
    your queries to ensure that you do not
    exceed our limits should that happen.

    https://www.coingecko.com/en/api#explore-api
    '''

    def __init__(self, debug=False):
        super(CoinGeckoClient, self).__init__(
            base_url='https://api.coingecko.com/api',
            debug=debug)

    def getCoinsList(self):
        path = '/v3/coins/list'
        coins = self._request(path, exceptions=True, json=True)
        return coins

    def getCoinsMarkets(self, vs_currency='usd', ids=''):
        path = '/v3/coins/markets'
        kwargs = {
            'vs_currency': vs_currency,
            'ids': ids,
            'page': 1,
            'per_page': 250}
        coins = []
        while True:
            tmp = self._request(
                path, exceptions=True, json=True, **kwargs)
            if not len(tmp):
                break
            coins.extend(tmp)
            kwargs['page'] += 1
        return coins

    def getCoinsHistory(self, id, date, localization=False):
        path = f'/v3/coins/{id}/history'
        kwargs = {
            'date': date,
            'localization': 'false' if not localization else 'true'}
        history = self._request(path, exceptions=True, json=True, **kwargs)
        return history

    def getCoinsMarketChart(self, id, vs_currency, days):
        path = f'/v3/coins/{id}/market_chart'
        kwargs = {
            'vs_currency': vs_currency,
            'days': days}
        mchart = self._request(path, exceptions=True, json=True, **kwargs)
        return mchart

    def getCoinsMarketChartRange(self, id, vs_currency, date_from, date_to):
        # date: timestamp ex: 1422577232
        path = f'/v3/coins/{id}/market_chart/range'
        kwargs = {
            'vs_currency': vs_currency,
            'from': date_from,
            'to': date_to}
        mchart = self._request(path, exceptions=True, json=True, **kwargs)
        return mchart

    def getExchangesList(self):
        path = '/v3/coins/exchanges'
        exchanges = self._request(path, exceptions=True, json=True)
        return exchanges