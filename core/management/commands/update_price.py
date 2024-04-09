import os

import json
import requests
from dotenv import load_dotenv


from django.core.management import BaseCommand

from core.models import Coin

load_dotenv()


def update_price():
    headers = {
        'x-access-token': os.getenv('COINRANKING_API_KEY')
    }

    all_coin = Coin.objects.filter(is_api=True)

    if len(all_coin) > 0:
        for coin in all_coin:
            print(coin.coin_name)
            if coin.is_api and coin.uuid:
                print(f"https://api.coinranking.com/v2/coin/{coin.uuid}")

                response = requests.request(
                    "GET",
                    f"https://api.coinranking.com/v2/coin/{coin.uuid}",
                    headers=headers
                )


                data = json.loads(response.text)
                print(f"https://api.coinranking.com/v2/coin/{coin.uuid}")
                print(data)

                if data['status'] == 'fail':
                    continue
                if data['data']['coin']['price'] == None:
                    continue

                coin.price = float(data['data']['coin']['price'])
                coin.coin_name = data['data']['coin']['name']
                coin.coin_symbol = data['data']['coin']['symbol']
                coin.market_cap = round(float(data['data']['coin']['marketCap']), 2)
                coin.save()
        return 'Done'
    else:
        return 'No data'


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_price()
