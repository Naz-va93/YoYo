import os

import json
import requests
from dotenv import load_dotenv


from django.core.management import BaseCommand

from core.models import Coin

load_dotenv()


def update_price_change_24h():
    headers = {
        'x-access-token': os.getenv('COINRANKING_API_KEY')
    }

    all_coin = Coin.objects.filter(is_api=True)

    if len(all_coin) > 0:
        for coin in all_coin:
            print(coin.coin_name)
            if coin.is_api and coin.uuid:
                print(f"https://api.coinranking.com/v2/coin/{coin.uuid}")

                response_price = requests.request(
                    "GET",
                    f"https://api.coinranking.com/v2/coin/{coin.uuid}/history",
                    headers=headers
                )

                data_price_24 = json.loads(response_price.text)

                if data_price_24['status'] == 'fail':
                    continue

                if data_price_24['data']['change'] != None:
                    coin.price_24h = round(float(data_price_24['data']['change']), 2)

                coin.save()
        return 'Done'
    else:
        return 'No data'


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_price_change_24h()
