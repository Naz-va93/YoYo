from datetime import datetime, timedelta

from django.utils.timezone import make_aware

from core.models import Setting
from core.models import Category, NetworkChain, Type, Social
from user.models import User


def context_controller(request):
    settings = Setting.get_settings()

    context = {
        'settings': settings,
        'socials': Social.objects.all(),
    }
    context['categories'] = Category.objects.all()
    context['chains'] = NetworkChain.objects.all()
    context['types'] = Type.objects.all()

    return context


def time_until_next_vote(request):
    result = None
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)
        if user.first_vote:
            now = make_aware(datetime.now())
            time_difference = now - user.first_vote
            remaining_time = timedelta(hours=12) - time_difference
            remaining_hours = round(remaining_time.total_seconds() / 3600)
            result = max(remaining_hours, 0)

            if result == 0:
                result = 0.5

    return {'time_until_next_vote': result}
