from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	vote_coins = models.ManyToManyField('core.Coin', verbose_name='Голоса за коины', blank=True)
	vote_count = models.IntegerField('Количество голосов', default=5)
	last_vote = models.DateTimeField(null=True, blank=True, verbose_name='Дата последнего голоса')
