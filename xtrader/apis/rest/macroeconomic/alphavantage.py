from typing import Any, Union
from xtrader.apis.utils import call_api


BASE_URL = 'https://www.alphavantage.co/query?'

AQ_INTERVALS = ['annual', 'quarterly']
DWM_INTERVALS = ['daily', 'weekly', 'monthly']
MS_INTERVALS = ['monthly', 'semiannual']
YIELD_MATURITIES = ['3month', '2year', '5year', '7year', '10year', '30year']


class AlphaVantageMacroAPI:
    """
    Retrieved from FRED, Federal Reserve Bank of St. Louis.
    This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis.
    By using this data feed, you agree to be bound by the FRED® API Terms of Use.
    """

    def __init__(self, api_key):
        """ Initialize the class with a valid AlphaVantage API key."""
        self.api_key = api_key


    def get_real_gdp(self, country: str = 'USA', interval: str = 'annual') -> Any:
        """
        This API returns the annual and quarterly Real GDP of the United States.

        :param interval: 'annual' or 'quarterly'
        """
        if country != 'USA':
            raise ValueError('AlphaVantageMacroAPI only supports USA for now.')
        if interval not in ['annual', 'quarterly']:
            raise ValueError(f'`interval` must be one of: {AQ_INTERVALS}')
        
        params = {'function': 'REAL_GDP', 'interval': interval, 'apikey': self.api_key}
        return call_api(BASE_URL, params=params)
    

    def get_real_gdp_per_capita(self, country: str = 'USA') -> Any:
        """ This API returns the annual and quarterly Real GDP per capita of the United States. """
        if country != 'USA':
            raise ValueError('AlphaVantageMacroAPI only supports USA for now.')
        
        params = {'function': 'REAL_GDP_PER_CAPITA', 'apikey': self.api_key}
        return call_api(base_url=BASE_URL, params=params)
    

    def get_treasury_yield(self, country: str = 'USA', interval='monthly', maturity='10year') -> Any:
        """
        This API returns the daily, weekly, and monthly US treasury yield of
        a given maturity timeline (e.g., 5 year, 30 year, etc).

        :param interval: 'daily', 'weekly', or 'monthly'
        :param maturity: '3month', '2year', '5year', '7year', '10year', '30year'
        """
        if interval not in DWM_INTERVALS:
            raise ValueError(f'`interval` must be one of: {DWM_INTERVALS}')
        if maturity not in YIELD_MATURITIES:
            raise ValueError(f'`maturity` must be one of: {YIELD_MATURITIES}')
        
        params = {'function': 'TREASURY_YIELD', 'interval': interval,
                  'maturity': maturity, 'apikey': self.api_key}
        return call_api(base_url=BASE_URL, params=params)
    

    def get_fed_funds_rate(self, interval: str = 'monthly') -> Union[Any, str]:
        """
        Returns the daily, weekly, and monthly federal funds rate (interest rate) of the United States.
        
        :param interval: 'daily', 'weekly', or 'monthly'
        """
        if interval not in DWM_INTERVALS:
            raise ValueError(f'`interval` must be one of: {DWM_INTERVALS}')

        params = {'function': 'FEDERAL_FUNDS_RATE', 'interval': interval, 'apikey': self.api_key}
        return call_api(base_url=BASE_URL, params=params)
    

    def get_cpi(self, country: str = 'USA', interval: str = 'monthly') -> Any:
        """
        Returns the monthly and semiannual consumer price index (CPI) of the United States.
        CPI is widely regarded as the barometer of inflation levels in the broader economy.

        :param interval: 'monthly'
        """
        if interval != 'monthly':
            raise ValueError(f'`interval` must be one of: {MS_INTERVALS}')
        
        params = {'function': 'CPI', 'interval': interval, 'apikey': self.api_key}
        return call_api(base_url=BASE_URL, params=params)
    

    def get_inflation(self, country: str = 'USA') -> Any:
        """ Returns the annual and quarterly inflation rate of the United States. """
        if country != 'USA':
            raise ValueError('AlphaVantageMacroAPI only supports USA for now.')
        
        params = {'function': 'INFLATION', 'apikey': self.api_key}
        return call_api(base_url=BASE_URL, params=params)
    

    def get_retail_sales(self, country='USA') -> Any:
        """ Returns the monthly Advance Retail Sales: Retail Trade data of the United States. """
        if country != 'USA':
            raise ValueError('AlphaVantageMacroAPI only supports USA for now.')
        
        params = {'function': 'RETAIL_SALES', 'apikey': self.api_key}
        return call_api(base_url=BASE_URL, params=params)
    

    def get_durables(self, country='USA') -> Any:
        """ This API returns the monthly manufacturers' new orders of durable goods in the United States."""
        if country != 'USA':
            raise ValueError('AlphaVantageMacroAPI only supports USA for now.')
        
        params = {'function': 'DURABLES', 'apikey': self.api_key}
        return call_api(base_url=BASE_URL, params=params)


    def get_unemployment(self, country='USA') -> Any:
        """ 
        returns the monthly unemployment data of the United States.
        The unemployment rate represents the number of unemployed as a percentage of the labor force.
        """
        if country != 'USA':
            raise ValueError('AlphaVantageMacroAPI only supports USA for now.')
        
        params = {'function': 'UNEMPLOYMENT', 'apikey': self.api_key}
        return call_api(base_url=BASE_URL, params=params)
    

    def get_nonfarm_payroll(self, country='USA') -> Any:
        """
        Returns the monthly US All Employees: Total Nonfarm (commonly known as Total Nonfarm Payroll),
        a measure of the number of U.S. workers in the economy that excludes proprietors, private household employees,
        unpaid volunteers, farm employees, and the unincorporated self-employed.
        """
        if country != 'USA':
            raise ValueError('AlphaVantageMacroAPI only supports USA for now.')
        
        params = {'function': 'NONFARM_PAYROLL', 'apikey': self.api_key}
        return call_api(base_url=BASE_URL, params=params)
        