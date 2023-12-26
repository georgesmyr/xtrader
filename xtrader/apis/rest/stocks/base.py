from abc import ABC, abstractmethod

class BaseStockAPI:

    @abstractmethod
    def get_daily(self, symbol, **kwargs):
        pass

    @abstractmethod
    def get_intraday(self, symbol, **kwargs):
        pass

    @abstractmethod
    def get_weekly(self, symbol, **kwargs):
        pass

    @abstractmethod
    def get_monthly(self, symbol, **kwargs):
        pass