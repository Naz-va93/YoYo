import time

import schedule
from django.core.management import BaseCommand

from core.models import Coin
from datetime import datetime

import json
import requests


def read_proxies_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]


def is_proxy_working(proxy):
    try:
        formatted_proxy = {'http': f'http://{proxy}'}
        response = requests.get('https://google.com', proxies=formatted_proxy, timeout=5)
        return response.status_code == 200
    except:
        return False


def get_working_proxy(proxies):
    for proxy in proxies:
        if is_proxy_working(proxy):
            return proxy
    return None

def update_price():
    headers = {
        'x-access-token': 'coinrankingb1ae851b47d9980db2f592791290cc97ddf42500035cbc36'
    }
    proxy_list = read_proxies_from_file('/var/www/coinjojo/proxy_list.txt')

    working_proxy = get_working_proxy(proxy_list)

    proxy_config = {'https': f'http://{working_proxy}'} if working_proxy else None
    all_coin = Coin.objects.filter(is_api=True)

    if len(all_coin) > 0:
        for coin in all_coin:
            print(coin.coin_name)
            print(proxy_config)
            if coin.is_api and coin.uuid:
                print(f"https://api.coinranking.com/v2/coin/{coin.uuid}")
                response = requests.request("GET", f"https://api.coinranking.com/v2/coin/{coin.uuid}", headers=headers, proxies=proxy_config)
                response_price = requests.request("GET", f"https://api.coinranking.com/v2/coin/{coin.uuid}/history?timePeriod=1y", headers=headers, proxies=proxy_config)
                data = json.loads(response.text)
                print(f"https://api.coinranking.com/v2/coin/{coin.uuid}")
                print(data)
                data_price_24 = json.loads(response_price.text)

                if data['status'] == 'fail':
                    continue
                if data['data']['coin']['price'] == None:
                    continue
                coin.price = float(data['data']['coin']['price'])
                if data_price_24['status'] == 'fail':
                    continue
                if data_price_24['data']['history'][0]['price'] != None:
                    result = float(data_price_24['data']['history'][0]['price']) - coin.price
                    result = round(result / coin.price * 100, 2)
                    coin.price_24h = result

                coin.coin_name = data['data']['coin']['name']
                coin.coin_symbol = data['data']['coin']['symbol']
                coin.market_cap = round(float(data['data']['coin']['marketCap']), 2)
                coin.save()
        return 'Done'
    else:
        return 'No data'


class Command(BaseCommand):
    def handle(self, *args, **options):
        date = datetime.now()
        while True:
            update_price()
            time.sleep(60)
