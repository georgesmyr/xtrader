from abc import ABC, abstractmethod

class BaseCryptoAPI:

    @abstractmethod
    def call_api(self, endpoint: str):
        pass

    @abstractmethod
    def get_exchange_rate(self, from_currency: str, to_currency: str):
        pass

    @abstractmethod
    def get_intraday(self, symbol: str, **kwargs):
        pass

    @abstractmethod
    def get_daily(self, symbol: str, **kwargs):
        pass

    @abstractmethod
    def get_weekly(self, symbol: str, **kwargs):
        pass

    @abstractmethod
    def get_monthly(self, symbol: str, **kwargs):
        pass