import json
from datetime import datetime
from Trader import Trader


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


def main():
    trader = Trader.with_budget_in_usd(1000)

    sentiment = get_sentiment('btc_sentiment.json')
    prices = get_stock_prices('btc_price.json')
    dates = get_ordered_dates(sentiment, prices)

    for date in dates:
        print("Date {} with price {} USDT and sentiment {}".format(date, prices[date], sentiment[date]))
        trader.update(prices[date], sentiment[date])
        print("Status after:{} USDT, {} BTC".format(str(trader.USDT), str(trader.BTC)))
        print()

    print("Final result: {} USD".format(round(trader.to_usdt(), 2)))


if __name__ == '__main__':
    main()

