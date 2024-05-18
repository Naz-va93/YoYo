import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


def get_currency_price_to_usd(currency):
    headers = {
        'x-access-token': os.getenv('COINRANKING_API_KEY')
    }

    usd_uuid = 'yhjMzLPhuIDl'

    if currency.uuid == usd_uuid:
        return 1

    response = requests.request(
        "GET",
        f"https://api.coinranking.com/v2/coin/{usd_uuid}/price?referenceCurrencyUuid={currency.uuid}",
        headers=headers
    )

    data = json.loads(response.text)

    if data['status'] == 'success':
        if data['data'].get('price'):
            return float(data['data']['price'])

    return 0


def update_currency_price_to_usd(currency):
    price_to_usd = get_currency_price_to_usd(currency)
    if price_to_usd:
        currency.price_to_usd = round(price_to_usd, 2)
        currency.save()
