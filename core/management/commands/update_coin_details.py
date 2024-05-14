import os

import json
import time
from datetime import datetime

import pandas as pd
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

        time.sleep(0.1)


def update_coin_details_uniswap(coins):
    UNISWAP_V3_SUBGRAPH_URL = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"

    def run_query(query):
        try:
            response = requests.post(UNISWAP_V3_SUBGRAPH_URL, json={'query': query})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Query failed: {e}")
            return None

    def get_current_price(token_address):
        query = f"""
        {{
          token(id: "{token_address}") {{
            derivedETH
          }}
          bundle(id: "1") {{
            ethPriceUSD
          }}
        }}
        """
        result = run_query(query)
        if result:
            token_data = result['data']['token']
            eth_price = float(result['data']['bundle']['ethPriceUSD'])
            price_usd = float(token_data['derivedETH']) * eth_price
            return price_usd
        return None

    def get_volume_24h(token_address):
        query = f"""
        {{
          tokenDayDatas(first: 1, orderBy: date, orderDirection: desc, where: {{ token: "{token_address}" }}) {{
            volumeUSD
          }}
        }}
        """
        result = run_query(query)
        if result:
            return float(result['data']['tokenDayDatas'][0]['volumeUSD'])
        return None

    def get_price_change_24h(token_address):
        query = f"""
        {{
          tokenHourDatas(first: 25, orderBy: periodStartUnix, orderDirection: desc, where: {{ token: "{token_address}" }}) {{
            close: priceUSD
          }}
        }}
        """
        result = run_query(query)
        if result and len(result['data']['tokenHourDatas']) >= 25:
            latest_price = float(result['data']['tokenHourDatas'][0]['close'])
            previous_price = float(result['data']['tokenHourDatas'][24]['close'])
            price_change_24h = ((latest_price - previous_price) / previous_price) * 100
            return round(price_change_24h, 2)
        return None

    def get_max_price_and_date(token_address):
        all_data = []
        skip = 0
        has_more_data = True

        while has_more_data:
            query = f"""
            {{
              tokenDayDatas(first: 1000, skip: {skip}, orderBy: date, orderDirection: desc, where: {{ token: "{token_address}" }}) {{
                date
                high
              }}
            }}
            """
            result = run_query(query)
            if result and 'data' in result and 'tokenDayDatas' in result['data']:
                data = result['data']['tokenDayDatas']
                if data:
                    all_data.extend(data)
                    skip += 1000
                else:
                    has_more_data = False
            else:
                has_more_data = False

        if all_data:
            df = pd.DataFrame(all_data)
            df['date'] = pd.to_datetime(df['date'], unit='s')
            df['high'] = df['high'].astype(float)

            max_price_row = df.loc[df['high'].idxmax()]
            max_price = max_price_row['high']
            max_price_date = max_price_row['date']
            return max_price, max_price_date

        return None, None

    for coin in coins:
        coin_id = coin.uuid.lower()

        current_price = get_current_price(coin_id)
        volume_24h = get_volume_24h(coin_id)
        price_change_24h = get_price_change_24h(coin_id)
        max_price, max_price_date = get_max_price_and_date(coin_id)

        if current_price is not None:
            coin.price = current_price
        if volume_24h is not None:
            coin.volume_24h = volume_24h
        if price_change_24h is not None:
            coin.price_24h = price_change_24h
        if max_price is not None and max_price_date is not None:
            coin.all_time_high = max_price
            coin.all_time_high_date = max_price_date

        coin.save()

        time.sleep(0.2)


def update_coin_details():
    coins_with_coinranking_api = Coin.objects.filter(is_api=True, api='coinranking')
    if len(coins_with_coinranking_api) > 0:
        for coin in coins_with_coinranking_api:
            update_coin_details_coinranking(coin)

    coins_with_uniswap_api = Coin.objects.filter(is_api=True, api='uniswap')
    if len(coins_with_uniswap_api) > 0:
        update_coin_details_uniswap(coins_with_uniswap_api)


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_coin_details()
