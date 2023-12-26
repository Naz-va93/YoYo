from core.models import Setting
from core.models import Category, NetworkChain, Type, Social


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