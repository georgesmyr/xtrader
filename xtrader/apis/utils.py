import requests

def call_api(base_url: str, params: dict):
        """ Requests data from the API and returns the response."""
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response