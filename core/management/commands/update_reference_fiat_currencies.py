import time

from django.core.management import BaseCommand

from core.management.commands.utils import update_currency_price_to_usd
from core.models import ReferenceCurrency


def update_currency_details():
    currencies = ReferenceCurrency.objects.filter(currency_type='fiat')

    for currency in currencies:
        update_currency_price_to_usd(currency)
        time.sleep(0.2)


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_currency_details()
