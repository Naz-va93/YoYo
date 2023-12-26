from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse

from core.models import Coin


def increment_favorite(request, pk):
    coin = get_object_or_404(Coin, pk=pk)
    user = request.user
    previous_page = request.GET.get('previous_page')

    if user.is_authenticated:
        if user in coin.favorite.all():
            coin.favorite.remove(user.pk)
            coin.save()
        else:
            coin.favorite.add(user.pk)
            coin.save()

    if previous_page:
        redirect_url = previous_page
    else:
        redirect_url = reverse('core:index')

    return redirect(redirect_url)


def increment_favorite_ajax(request, pk):
    coin = get_object_or_404(Coin, pk=pk)
    user = request.user
    previous_page = request.GET.get('previous_page')

    if user.is_authenticated:
        if user in coin.favorite.all():
            coin.favorite.remove(user.pk)
            coin.save()
        else:
            coin.favorite.add(user.pk)
            coin.save()

    if previous_page:
        redirect_url = previous_page
    else:
        redirect_url = reverse('core:index')

    return render(request, redirect_url)
