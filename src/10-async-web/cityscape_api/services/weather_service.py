import requests
import aiohttp
__api_key = ''


def global_init(api_key: str):
    global __api_key
    __api_key = api_key


def get_current(zip_code: str, country_code: str) -> dict:
    url = f'https://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&appid={__api_key}'
    resp = requests.get(url)
    resp.raise_for_status()

    return resp.json()


async def get_current_by_geo(lat: str, lon: str) -> dict:

    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={__api_key}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return data
