import time

import schedule
from django.core.management import BaseCommand

from core.models import Coin
from datetime import datetime


def clear():
    all_coin = Coin.objects.filter()
    for coin in all_coin:
        coin.votes_today = 0
        coin.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        date = datetime.now()

        print(date.hour)
        print(date.minute)
        while True:
            if date.hour == 1 and date.minute == 0:
                clear()
            time.sleep(40)
