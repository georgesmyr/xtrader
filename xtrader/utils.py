import requests

def call_api(endpoint: str):
        response = requests.get(endpoint)
        if response.status_code != 200:
            raise ValueError(f'Invalid API response: {response}')
        return response