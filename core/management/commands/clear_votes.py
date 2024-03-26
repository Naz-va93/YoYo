import time
from django.core.management import BaseCommand
from core.models import Coin


def clear():
    all_coin = Coin.objects.filter()
    for coin in all_coin:
        coin.votes_today = 0
        coin.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        clear()
