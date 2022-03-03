class BalanceTrader:
    BTC = 0
    USDT = 0
    btc_price = 0
    btc_factor = 0

    @staticmethod
    def with_budget_in_usd(usd, btc_factor=0.6):
        trader = BalanceTrader()
        trader.USDT = usd
        trader.BTC = 0
        trader.btc_price = 0
        trader.btc_factor = btc_factor
        return trader

    def sell_btc(self, usdt):
        self.BTC -= usdt / self.btc_price
        self.USDT += usdt

    def buy_btc(self, usdt):
        self.BTC += usdt / self.btc_price
        self.USDT -= usdt

    def decision(self):
        btc_in_usdt = self.BTC * self.btc_price
        money = btc_in_usdt + self.USDT

        usdt_percentage = self.USDT / money

        target_usdt = (1.0 - self.btc_factor) * self.USDT / usdt_percentage

        if target_usdt > self.USDT:
            self.sell_btc(target_usdt - self.USDT)
        else:
            self.buy_btc(self.USDT - target_usdt)

    def update(self, price, sentiment=None):
        self.btc_price = price
        self.decision()

    def to_usdt(self):
        return self.USDT + self.btc_price * self.BTC


class FearAndGreedTrader:
    BTC = 0
    USDT = 0
    btc_price = 0

    @staticmethod
    def with_budget_in_usd(usd):
        trader = FearAndGreedTrader()
        trader.USDT = usd
        trader.BTC = 0
        trader.btc_price = 0
        return trader

    def sell_btc(self, minimum, percentage):
        trade = max(self.btc_price / minimum, percentage * self.BTC)

        if self.BTC > trade:
            self.BTC -= trade
            self.USDT += trade * self.btc_price
            print("\tSell {} BTC".format(trade))
        else:
            print("\tNo budget to SELL")

    def hold(self):
        print("\tHold !")

    def buy_btc(self, minimum, percentage):
        trade = max(minimum, percentage * self.USDT)

        if self.USDT > trade:
            self.USDT -= trade
            self.BTC += trade / self.btc_price
            print("\tBuy using {} USDT".format(trade))
        else:
            print("\tNo budget to BUY")

    def decision(self, sentiment):
        if sentiment >= 80:
            self.sell_btc(1, 0.08)
            return

        if sentiment >= 60:
            self.sell_btc(0.5, 0.04)
            return

        if sentiment >= 40:
            self.hold()
            return

        if sentiment >= 20:
            self.buy_btc(0.5, 0.04)
            return

        self.buy_btc(1, 0.08)

    def update(self, price, sentiment):
        self.btc_price = price
        self.decision(sentiment)

    def to_usdt(self):
        return self.USDT + self.btc_price * self.BTC
