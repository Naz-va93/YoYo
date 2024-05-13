# from django.core.mail import send_mail
# from coinjojo.celery import app
#
# import json
# import requests
#
# from core.models import Coin
#
#
# def read_proxies_from_file(file_path):
#     with open(file_path, 'r') as file:
#         return [line.strip() for line in file.readlines() if line.strip()]
#
#
# def is_proxy_working(proxy):
#     try:
#         formatted_proxy = {'http': f'http://{proxy}'}
#         response = requests.get('https://google.com', proxies=formatted_proxy, timeout=5)
#         return response.status_code == 200
#     except:
#         return False
#
#
# def get_working_proxy(proxies):
#     for proxy in proxies:
#         if is_proxy_working(proxy):
#             return proxy
#     return None
#
#
# @app.task()
# def get_crypto_info_by_id():
#     headers = {
#         'x-access-token': 'coinrankingb1ae851b47d9980db2f592791290cc97ddf42500035cbc36'
#     }
#     proxy_list = read_proxies_from_file('/var/www/coinjojo/proxy_list.txt')
#
#     working_proxy = get_working_proxy(proxy_list)
#
#     proxy_config = {'https': f'http://{working_proxy}'} if working_proxy else None
#     all_coin = Coin.objects.filter(is_api=True)
#     if len(all_coin) > 0:
#         for coin in all_coin:
#             if coin.is_api:
#                 response = requests.request("GET", f"https://api.coinranking.com/v2/coin/{coin.uuid}", headers=headers,
#                                             proxies=proxy_config)
#                 response_price = requests.request("GET",
#                                                   f"https://api.coinranking.com/v2/coin/{coin.uuid}/history?timePeriod=1y",
#                                                   headers=headers, proxies=proxy_config)
#                 data = json.loads(response.text)
#                 data_price_24 = json.loads(response_price.text)
#                 coin.price_24h = data_price_24['data']['history']['price']
#                 coin.coin_name = data['data']['coin']['name']
#                 coin.price = round(float(data['data']['coin']['price']), 2)
#                 coin.coin_symbol = data['data']['coin']['symbol']
#                 coin.market_cap = round(float(data['data']['coin']['marketCap']), 2)
#                 coin.save()
#         return 'Done'
#     else:
#         return 'No data'


# @app.task()
# def clear_today_votes():
#     all_coin = Coin.objects.filter()
#     for coin in all_coin:
#         coin.votes_today = 0
#         coin.save()


"""@app.task()
def change_price_coin():
    headers = {
        'x-access-token': 'coinrankingb1ae851b47d9980db2f592791290cc97ddf42500035cbc36'
    }
    all_coin = Coin.objects.filter(is_api=True)
    if len(all_coin) > 0:
        for coin in all_coin:
            if coin.is_api:
                response = requests.request("GET", f"https://api.coinranking.com/v2/coin/{coin.uuid}", headers=headers)
                data = json.loads(response.text)
                coin.price = round(float(data['data']['coin']['price']), 2)
                coin.save()
        return 'Done'
    else:
        return 'No data'"""
