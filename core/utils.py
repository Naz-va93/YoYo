from datetime import timedelta, timezone

from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect, render

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import translate_url
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import check_for_language
from datetime import datetime

from core.models import Coin


def increment_counter(request, pk):
    coin = get_object_or_404(Coin, pk=pk)
    previous_page = request.POST.get('previous_page')

    if 'liked' in request.COOKIES:
        last_liked_time = datetime.fromtimestamp(float(request.COOKIES['liked']))
        time_since_last_like = datetime.now() - last_liked_time
        if time_since_last_like.total_seconds() < 12 * 3600:
            if previous_page:
                return redirect(previous_page)
            else:
                return redirect('core:index')
    else:
        Vote.objects.create(coin=coin)
        expires = datetime.utcnow() + timedelta(hours=12)
        response = redirect('core:index')
        response.set_cookie('liked', str(datetime.now().timestamp()), expires=expires)
        return response
    if previous_page:
        return redirect(previous_page)
    else:
        return redirect('core:index')


def increment_metrik(request, slug):
    coin = get_object_or_404(Coin, slug=slug)
    if coin.counter_link_usage or coin.counter_link_usage == 0:
        coin.counter_link_usage += 1
    else:
        coin.counter_link_usage = 0
    coin.save()


def custom_set_language(request):
    next_url = None
    if (
            next_url or request.accepts("text/html")
    ) and not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = request.META.get("HTTP_REFERER")
        if not url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
        ):
            next_url = "/"
    response = HttpResponseRedirect(next_url) if next_url else HttpResponse(status=204)

    lang_code = request.GET.get('lang')
    if lang_code and check_for_language(lang_code):
        if next_url:
            next_trans = translate_url(next_url, lang_code)
            if next_trans != next_url:
                response = HttpResponseRedirect(next_trans)
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            lang_code,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )
    return response

def search_coins_ajax(request):
    query = request.GET.get('q', '')

    coins = Coin.objects.filter(coin_name__icontains=query)[:3]

    results = []
    for coin in coins:
        results.append({
            'name': coin.coin_name,
            'url': coin.get_absolute_url()
        })

    return JsonResponse(results, safe=False)


def sort_filter_pagination_ajax(request):
    sort_direction = request.GET.get('sort_direction')
    sort_name = request.GET.get('sort_name')
    time_best = request.GET.get('time_best')
    category = request.GET.get('category')
    chain = request.GET.get('chain')
    type = request.GET.get('type')
    promote = request.GET.get('promote')
    page = request.GET.get('page')

    today = datetime.now()
    if not page:
        page = 2
    else:
        page = int(page)
        page *= 2


    coins = ''
    if promote:
        if sort_direction == 'asc':
            coins = Coin.objects.filter(is_moderate=True, promoted_status=True).annotate(counter_like=Count('vote'),
                                                                                         counter_like_today=Count(
                                                                                             'vote',
                                                                                             filter=Q(
                                                                                                 vote__date_new__date=today))).order_by(
                f'-{sort_name}')
        elif sort_direction == 'desc':
            coins = Coin.objects.filter(is_moderate=True, promoted_status=True).annotate(counter_like=Count('vote'),
                                                                                         counter_like_today=Count(
                                                                                             'vote',
                                                                                             filter=Q(
                                                                                                 vote__date_new__date=today))).order_by(
                sort_name)

        if time_best == 'today':
            coins = Coin.objects.filter(is_moderate=True, promoted_status=True).annotate(counter_like=Count('vote'),
                                                                                         counter_like_today=Count(
                                                                                             'vote',
                                                                                             filter=Q(
                                                                                                 vote__date_new__date=today))).order_by(
                '-counter_like_today')
        elif time_best == 'all_time':
            coins = Coin.objects.filter(is_moderate=True, promoted_status=True).annotate(counter_like=Count('vote'),
                                                                                         counter_like_today=Count(
                                                                                             'vote',
                                                                                             filter=Q(
                                                                                                 vote__date_new__date=today))).order_by(
                '-counter_like')
    else:
        if sort_direction == 'asc':
            coins = Coin.objects.filter(is_moderate=True).annotate(counter_like=Count('vote'),
                                                                   counter_like_today=Count('vote',
                                                                                            filter=Q(
                                                                                                vote__date_new__date=today))).order_by(
                f'-{sort_name}')
        elif sort_direction == 'desc':
            coins = Coin.objects.filter(is_moderate=True).annotate(counter_like=Count('vote'),
                                                                   counter_like_today=Count('vote',
                                                                                            filter=Q(
                                                                                                vote__date_new__date=today))).order_by(
                sort_name)

        if time_best == 'today':
            coins = Coin.objects.filter(is_moderate=True).annotate(counter_like=Count('vote'),
                                                                   counter_like_today=Count('vote',
                                                                                            filter=Q(
                                                                                                vote__date_new__date=today))).order_by(
                '-counter_like_today')
        elif time_best == 'all_time':
            coins = Coin.objects.filter(is_moderate=True).annotate(counter_like=Count('vote'),
                                                                   counter_like_today=Count('vote',
                                                                                            filter=Q(
                                                                                                vote__date_new__date=today))).order_by(
                '-counter_like')

    if category:
        coins = coins.filter(category__slug=category)
    if chain:
        coins = coins.filter(chain__slug=chain)
    if type:
        coins = coins.filter(type__slug=type)


    if not coins:
        coins = Coin.objects.filter(is_moderate=True).annotate(counter_like=Count('vote'),
                                                               counter_like_today=Count('vote',
                                                                                        filter=Q(
                                                                                            vote__date_new__date=today))).order_by(
            '-counter_like')

    response = JsonResponse({'html': render(request, '_table-coins-item_1.html', {'coins': coins[page-2:page]}).content.decode('utf-8'),
                             'coin_counter': list(Paginator(coins, 2).page_range)})
    response['Access-Control-Allow-Origin'] = '*'
    return response


def increment_counter_like_ajax(request, pk):
    coin = get_object_or_404(Coin, pk=pk)
    previous_page = request.POST.get('previous_page')

    if 'liked' in request.COOKIES:
        last_liked_time = datetime.fromtimestamp(float(request.COOKIES['liked']))
        time_since_last_like = datetime.now() - last_liked_time
        if time_since_last_like.total_seconds() < 12 * 3600:
            if previous_page:
                return render(request, previous_page, {'coins': ''})
            else:
                return render(request, previous_page, {'coins': ''})
    else:
        Vote.objects.create(coin=coin)
        expires = datetime.utcnow() + timedelta(hours=12)
        response = redirect('core:index')
        response.set_cookie('liked', str(datetime.now().timestamp()), expires=expires)
     #   return JsonResponse('_table-coins-item.html', {'coins': coins}, request)
    return


def get_text_by_number(number):
    if number >= 1000000000000:
        return f'{round(number / 1000000000000, 1)} Trillion'
    elif number >= 1000000000:
        return f'{round(number / 1000000000, 1)} Billion'
    elif number >= 1000000:
        return f'{round(number / 1000000, 1)} Million'

    if number <= 0.001:
        subscript_dict = {
            '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
            '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉'
        }

        rounded_number = f"{round(number, 7):.7f}"
        if rounded_number.replace('0', '') == '.':
            full_number = f"{number:.1000f}".rstrip('0')
            if full_number.replace('0', '') == '.':
                return number

            cnt_0_fractional = 0
            while full_number.split('.')[1][cnt_0_fractional] == '0':
                cnt_0_fractional += 1

            number_part = full_number.split('.')[1][cnt_0_fractional-1:]
            nulls_part = f"0{''.join(subscript_dict[char] for char in str(cnt_0_fractional-1) if char in subscript_dict)}"
            return f"0.{nulls_part}{''.join(number_part[:6-(len(nulls_part)-1)])}".rstrip('0')

        else:
            cnt_0_fractional = 0
            while rounded_number.split('.')[1][cnt_0_fractional] == '0':
                cnt_0_fractional += 1

            if cnt_0_fractional > 3:
                number_part = rounded_number.split('.')[1][cnt_0_fractional - 1:]
                nulls_part = f"0{''.join(subscript_dict[char] for char in str(cnt_0_fractional - 1) if char in subscript_dict)}"
                return f"0.{nulls_part}{''.join(number_part)}"

            return f"{float(rounded_number):.5f}".rstrip('0')

    return str(round(number, 3 + (1 if number < 0.01 else 0)))


def num_of_zeros(n):
    s = '{:.16f}'.format(n).split('.')[1]
    return len(s) - len(s.lstrip('0'))



