import json
from datetime import datetime
from Trader import FearAndGreedTrader, BalanceTrader
import logging

logging.basicConfig(level=logging.INFO)


def get_sentiment(file_name):
    sentiment = {}
    with open(file_name, encoding='utf-8') as file:
        data = json.load(file)

        for elem in data['data']:
            date = datetime.fromtimestamp(int(elem['timestamp']))
            sentiment[date.date()] = int(elem['value'])

    return sentiment


def get_stock_prices(file_name):
    prices = {}
    with open(file_name, encoding='utf-8') as file:
        data = json.load(file)

        for elem in data['Data']['Data']:
            date = datetime.fromtimestamp(int(elem['time']))
            prices[date.date()] = (elem['high'] + elem['low']) / 2

    return prices


def get_ordered_dates(sentiment, prices):
    dates = list(sentiment.keys() & prices.keys())
    dates.sort()
    return dates


def main(budget):
    traders = [BalanceTrader.with_budget_in_usd(budget), FearAndGreedTrader.with_budget_in_usd(budget)]

    sentiment = get_sentiment('btc_sentiment.json')
    prices = get_stock_prices('btc_price.json')
    dates = get_ordered_dates(sentiment, prices)

    for trader in traders:
        for date in dates:
            trader.trade(prices[date], sentiment[date])
            logging.debug("Closing day: {} USDT, {} BTC".format(str(trader.usdt_in_wallet), str(trader.btc_in_wallet)))
        logging.info("Final result for {} is: {} USD".format(type(trader), round(trader.to_usdt(), 2)))


if __name__ == '__main__':
    main(1000)

