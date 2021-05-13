from __future__ import division, absolute_import, print_function

import backtrader as bt
import pandas as pd

from btconfig import BTConfigApiClient


class CoinMetricsClient(BTConfigApiClient):

    '''
    CoinMetrics Client

    https://docs.coinmetrics.io/api
    '''

    FMT = "%Y-%m-%dT%H:%M:%S"  # e.g. 2016-01-01T00:00:00
    FREQUENCY = {
        (bt.TimeFrame.Days, 1): '1d'
    }

    def __init__(self, debug=False):
        super(CoinMetricsClient, self).__init__(
            base_url='https://community-api.coinmetrics.io', debug=debug)

    def getAssetMetrics(
            self, assets, metrics, start_time=None, end_time=None,
            frequency='1d'):
        path = '/v4/timeseries/asset-metrics'
        kwargs = {
            'assets': assets,
            'metrics': metrics,
            'page_size': 10000,
            'frequency': frequency}
        if start_time:
            kwargs['start_time'] = start_time
        if end_time:
            kwargs['end_time'] = end_time
        res = []
        url = self._getUrl(path, **kwargs)
        while True:
            response = self._requestUrl(url)
            if response.status_code == 200:
                tmp = response.json()
                if not len(tmp['data']):
                    break
                res += tmp['data']
                if 'next_page_url' in tmp:
                    url = tmp['next_page_url']
                    continue
            else:
                raise Exception(f'{response.url}: {response.text}')
            break
        return res

    def getMarketCandles(
            self, markets, start_time=None, end_time=None, frequency='1d'):
        path = '/v4/timeseries/market-candles'
        kwargs = {
            'markets': markets,
            'page_size': 10000,
            'frequency': frequency}
        if start_time:
            kwargs['start_time'] = start_time
        if end_time:
            kwargs['end_time'] = end_time
        res = []
        url = self._getUrl(path, **kwargs)
        while True:
            response = self._requestUrl(url)
            if response.status_code == 200:
                tmp = response.json()
                if not len(tmp['data']):
                    break
                res += tmp['data']
                if 'next_page_url' in tmp:
                    url = tmp['next_page_url']
                    continue
            else:
                raise Exception(f'{response.url}: {response.text}')
            break
        return res

    def getAssets(self, assets=''):
        # Available assets
        path = '/v4/catalog/assets'
        kwargs = {'assets': assets}
        res = self._request(path, json=True, **kwargs)
        return res['data']

    def getPairs(self, pairs=''):
        # Available pairs
        path = '/v4/catalog/pairs'
        kwargs = {'pairs': pairs}
        res = self._request(path, json=True, **kwargs)
        return res['data']

    def getMetrics(self, metrics=''):
        # Available metrics
        path = '/v4/catalog/metrics'
        kwargs = {'metrics': metrics}
        res = self._request(path, json=True, **kwargs)
        return res['data']

    def getExchanges(self, exchanges=''):
        # Available exchanges
        path = '/v4/catalog/exchanges'
        kwargs = {'exchanges': exchanges}
        res = self._request(path, json=True, **kwargs)
        return res['data']

    def getMarkets(self, markets=''):
        # Available markets
        path = '/v4/catalog/markets'
        kwargs = {'markets': markets}
        res = self._request(path, json=True, **kwargs)
        return res['data']

    def getIndexes(self, indexes=''):
        # Available indexes
        path = '/v4/catalog/indexes'
        kwargs = {'indexes': indexes}
        res = self._request(path, json=True, **kwargs)
        return res['data']

    def getMarketCapitalization(self, assets):
        return self.getAssetMetrics(assets, 'CapMrktCurUSD')

    def getRealizedMarketCapitalization(self, assets):
        return self.getAssetMetrics(assets, 'CapRealUSD')

    def getMVRVRatio(self, assets):
        return self.getAssetMetrics(assets, 'CapMVRVCur')


def create_data_df(data):
    if data is None:
        return
    res = pd.DataFrame(data)
    res.time = pd.to_datetime(res.time)
    for c in ['price_open', 'price_close', 'price_high',
              'price_low', 'volume']:
        res[c] = pd.to_numeric(res[c])
    res.rename(
        columns={'price_open': 'open', 'price_close': 'close',
                 'price_high': 'high', 'price_low': 'low'},
        inplace=True)
    res.drop(columns=['market', 'vwap'], inplace=True)
    return res[['time', 'open', 'high', 'low', 'close', 'volume']]


def create_metrics_df(data, metrics_cols):
    res = pd.DataFrame(data)
    res.time = pd.to_datetime(res.time)
    for m in metrics_cols.keys():
        res[m] = pd.to_numeric(res[m])
    res.rename(columns=metrics_cols, inplace=True)
    res.drop(columns=['asset'], inplace=True)
    return res


def get_market_name(exchange='bitstamp', base='btc', quote='usd', type='spot'):
    market = f'{exchange}-{base}-{quote}-{type}'
    return market


def get_market_parts(market):
    exchange, base, quote, type = market.split('-')
    return exchange, base, quote, type