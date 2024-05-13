import os

import json
from datetime import datetime

import requests
from dotenv import load_dotenv

from django.core.management import BaseCommand

from core.models import Coin

load_dotenv()


def update_coin_details_coinranking(coin):
    if coin.is_api and coin.uuid:
        headers = {
            'x-access-token': os.getenv('COINRANKING_API_KEY')
        }

        response = requests.request(
            "GET",
            f"https://api.coinranking.com/v2/coin/{coin.uuid}",
            headers=headers
        )

        data = json.loads(response.text)

        if data['status'] == 'fail':
            print(f"Failed to update coin details for {coin.coin_name} ({coin.coin_symbol})")
            return

        if data['data']['coin'].get('price'):
            coin.price = float(data['data']['coin']['price'])

        if data['data']['coin'].get('change'):
            coin.price_24h = round(float(data['data']['coin']['change']), 2)

        if data['data']['coin'].get('name'):
            coin.coin_name = data['data']['coin']['name']

        if data['data']['coin'].get('symbol'):
            coin.coin_symbol = data['data']['coin']['symbol']

        if data['data']['coin'].get('marketCap'):
            coin.market_cap = float(data['data']['coin']['marketCap'])

        if data['data']['coin'].get('fullyDilutedMarketCap'):
            coin.fully_diluted_market_cap = float(data['data']['coin']['fullyDilutedMarketCap'])

        if data['data']['coin']['allTimeHigh'].get('price'):
            coin.all_time_high = float(data['data']['coin']['allTimeHigh']['price'])

        if data['data']['coin']['allTimeHigh'].get('timestamp'):
            all_time_high_date = datetime.fromtimestamp(data['data']['coin']['allTimeHigh']['timestamp'])
            coin.all_time_high_date = all_time_high_date.date()

        if data['data']['coin'].get('24hVolume'):
            coin.volume_24h = float(data['data']['coin']['24hVolume'])

        coin.save()


def update_coin_details_uniswap(coin):
    pass


def update_coin_details():
    coins_with_coinranking_api = Coin.objects.filter(is_api=True, api='coinranking')
    if len(coins_with_coinranking_api) > 0:
        for coin in coins_with_coinranking_api:
            update_coin_details_coinranking(coin)

    coins_with_uniswap_api = Coin.objects.filter(is_api=True, api='uniswap')
    if len(coins_with_uniswap_api) > 0:
        for coin in coins_with_uniswap_api:
            update_coin_details_uniswap(coin)


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_coin_details()
