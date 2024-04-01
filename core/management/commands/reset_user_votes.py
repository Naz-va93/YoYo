from datetime import timedelta

from django.core.management import BaseCommand
from django.utils import timezone

from user.models import User


def reset_user_votes():
    twelve_hours_ago = timezone.now() - timedelta(hours=12)

    users_to_update = User.objects.filter(first_vote__lte=twelve_hours_ago)

    for user in users_to_update:
        user.vote_count = 5
        user.first_vote = None
        user.save()
        user.vote_coins.clear()


class Command(BaseCommand):
    def handle(self, *args, **options):
        reset_user_votes()
