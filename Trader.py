from abc import ABC, abstractmethod
import logging


class Trader(ABC):

    def __init__(self):
        self.btc_in_wallet = 0
        self.usdt_in_wallet = 0
        self.btc_price = 0

    def trade(self, price, sentiment):
        self.btc_price = price
        self.take_decision(sentiment)

    @abstractmethod
    def take_decision(self, sentiment):
        pass

    def to_usdt(self):
        return self.usdt_in_wallet + self.btc_price * self.btc_in_wallet


class BalanceTrader(Trader):

    @staticmethod
    def with_budget_in_usd(usd, btc_factor=0.6):
        trader = BalanceTrader()
        trader.usdt_in_wallet = usd
        trader.btc_in_wallet = 0
        trader.btc_price = 0
        trader.btc_factor = btc_factor
        return trader

    def sell_btc(self, usdt):
        self.btc_in_wallet -= usdt / self.btc_price
        self.usdt_in_wallet += usdt

    def buy_btc(self, usdt):
        self.btc_in_wallet += usdt / self.btc_price
        self.usdt_in_wallet -= usdt

    def take_decision(self, sentiment):
        btc_in_usdt = self.btc_in_wallet * self.btc_price
        money = btc_in_usdt + self.usdt_in_wallet

        usdt_percentage = self.usdt_in_wallet / money

        target_usdt = (1.0 - self.btc_factor) * self.usdt_in_wallet / usdt_percentage

        if target_usdt > self.usdt_in_wallet:
            self.sell_btc(target_usdt - self.usdt_in_wallet)
        else:
            self.buy_btc(self.usdt_in_wallet - target_usdt)


class FearAndGreedTrader(Trader):

    @staticmethod
    def with_budget_in_usd(usd):
        trader = FearAndGreedTrader()
        trader.usdt_in_wallet = usd
        trader.btc_in_wallet = 0
        trader.btc_price = 0
        return trader

    def sell_btc(self, minimum, percentage):
        trade = max(self.btc_price / minimum, percentage * self.btc_in_wallet)

        if self.btc_in_wallet > trade:
            self.btc_in_wallet -= trade
            self.usdt_in_wallet += trade * self.btc_price

    def buy_btc(self, minimum, percentage):
        trade = max(minimum, percentage * self.usdt_in_wallet)

        if self.usdt_in_wallet > trade:
            self.usdt_in_wallet -= trade
            self.btc_in_wallet += trade / self.btc_price

    def take_decision(self, sentiment):
        if sentiment >= 80:
            self.sell_btc(1, 0.08)
            return

        if sentiment >= 60:
            self.sell_btc(0.5, 0.04)
            return

        if sentiment >= 40:
            return

        if sentiment >= 20:
            self.buy_btc(0.5, 0.04)
            return

        self.buy_btc(1, 0.08)

