import requests, json
from typing import Optional
from datetime import datetime

class AlphaVantageFundamentalsAPI:

    def __init__(self, api_key):
        self.api_key = api_key

    
    def call_api(self, endpoint: str) -> json:
        response = requests.get(endpoint)
        if response.status_code != 200:
            raise ValueError(f'Invalid API response: {response}')
        return response
    

    def get_company_overview(self, symbol: str) -> json:
        """ 
        Returns the company information, financial ratios, and other key metrics for the equity specified.
        Data is generally refreshed on the same day a company reports its latest earnings and financials. 
        """
        endpoint = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={self.api_key}"
        return self.call_api(endpoint)
    

    def get_income_statement(self, symbol: str) -> json:
        """
        Returns the annual and quarterly income statements for the company of interest,
        with normalized fields mapped to GAAP and IFRS taxonomies of the SEC.
        Data is generally refreshed on the same day a company reports its latest earnings and financials.
        """
        endpoint = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={self.api_key}"
        return self.call_api(endpoint)
    
    
    def get_balance_sheet(self, symbol: str) -> json:
        """
        Returns the annual and quarterly balance sheets for the company of interest,
        with normalized fields mapped to GAAP and IFRS taxonomies of the SEC.
        Data is generally refreshed on the same day a company reports its latest earnings and financials.
        """
        endpoint = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={self.api_key}"
        return self.call_api(endpoint)
    

    def get_cash_flow(self, symbol: str) -> json:
        """
        Returns the annual and quarterly cash flows for the company of interest,
        with normalized fields mapped to GAAP and IFRS taxonomies of the SEC.
        Data is generally refreshed on the same day a company reports its latest earnings and financials.
        """
        endpoint = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={self.api_key}"
        return self.call_api(endpoint)
    

    def get_earnings(self, symbol: str) -> json:
        """
        Returns the annual and quarterly earnings (EPS) for the company of interest.
        Quarterly data also includes analyst estimates and surprise metrics.
        """
        endpoint = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey={self.api_key}"
        return self.call_api(endpoint)
    

    def get_listing_delisting_status(self, date: Optional[str]=None, state: Optional[str]='active') -> json:
        """
        Returns a list of active or delisted US stocks and ETFs, either as of the latest trading day or at a specific time in history.
        The endpoint is positioned to facilitate equity research on asset lifecycle and survivorship.

        :param date: If no date is set, the API endpoint will return a list of active or delisted symbols as of the latest trading day.
                     If a date is set, the API endpoint will "travel back" in time and return a list of active or delisted symbols on that particular date in history.
                     Any YYYY-MM-DD date later than 2010-01-01 is supported. For example, date=2013-08-03
        :param state: By default, state=active and the API will return a list of actively traded stocks and ETFs.
                      Set state=delisted to query a list of delisted assets.
        """
        if state not in ['active', 'delisted']:
            raise ValueError(f'`state` must be one of: {state}')
        
        endpoint = f"https://www.alphavantage.co/query?function=LISTING_STATUS"
        if date is not None:
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except:
                raise ValueError(f'`date` must be in YYYY-MM-DD format: {date}')
            endpoint += f"&date={date}"
        if state == 'delisted':
            endpoint += '&state=delisted'
        endpoint += f"&apikey={self.api_key}"

        return self.call_api(endpoint)
    

    def get_ipo_calendar(self) -> json:
        """
        Returns the initial public offering (IPO) and lockup expiration dates for US equity markets.
        """
        endpoint = f"https://www.alphavantage.co/query?function=IPO_CALENDAR&apikey={self.api_key}"
        return self.call_api(endpoint)
    

    def get_earnings_calendar(self, symbol: Optional[str]=None, horizon: Optional[str]='3months') -> json:
        """
        Returns a list of company earnings expected in the next 3, 6, or 12 months.

        :param symbol: By default, no symbol will be set for this API. When no symbol is set,
                       the API endpoint will return the full list of company earnings scheduled.
                       If a symbol is set, the API endpoint will return the expected earnings for that specific symbol.
        :param horizon: By default, horizon=3month and the API will return a list of expected company earnings in the next 3 months.
                        You may set horizon=6month or horizon=12month to query the earnings scheduled for the next 6 months or 12 months, respectively.
        """
        if horizon not in ['3month', '6month', '12month']:
            raise ValueError(f'`horizon` must be one of: {horizon}')
        endpoint = f"https://www.alphavantage.co/query?function=EARNINGS_CALENDAR"
        if symbol:
            endpoint += f"&symbol={symbol}"
        if horizon:
            endpoint += f"&horizon={horizon}"
        endpoint += f"&apikey={self.api_key}"

        return self.call_api(endpoint)
        
