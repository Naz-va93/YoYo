from django.core.management import BaseCommand

from user.models import User


def reset_user_votes():
    User.objects.all().update(vote_count=5, first_vote=None)

    for user in User.objects.all():
        user.vote_coins.clear()


class Command(BaseCommand):
    def handle(self, *args, **options):
        reset_user_votes()
