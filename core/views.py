import os
from datetime import datetime, timedelta

import requests
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Count, Q, When, Case, BooleanField

from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from dotenv import load_dotenv

from core.forms import CreateCoin, CaptchaForm
from core.models import Coin, Category, NetworkChain, ListingPlatform, Page, Type, Social, Listing, AdvertisingItem, \
    Banner
from core.utils import increment_metrik, increment_counter, get_text_by_number, convert_period_to_days

load_dotenv()


def page(request, slug):
    context = {
        'page': Page.objects.get(slug=slug)
    }
    return render(request, 'privacy-police.html', context=context)


def coin_list(request, slug):
    listing = Listing.objects.get(slug=slug)
    coins = listing.get_coins()

    is_paginated = True
    disable_filter = False
    if listing.filter_by == 'new' or listing.filter_by == 'promote':
        coins = coins[:30]
        is_paginated = False
        disable_filter = True
    else:
        p = Paginator(coins, 30)
        page_num = request.GET.get('page', 1)
        coins = p.page(page_num)

    context = {
        'listing': listing,
        'coins': coins,
        'is_paginated': is_paginated,
        'page': Page.objects.get(slug='coin-list'),
        'categories': Category.objects.all(),
        'chains': NetworkChain.objects.all(),
        'types': Type.objects.all(),
        'disable_filter': disable_filter,
    }
    return render(request, 'new-listing.html', context=context)


def get_coins_table(request):
    listing = Listing.objects.get(slug=request.GET.get('listing_slug'))
    coins = listing.get_coins()

    category = request.GET.get('category', 'all')
    network_chain = request.GET.get('network_chain', 'all')
    type_project = request.GET.get('type_project', 'all')

    if category != 'all':
        category = Category.objects.get(slug=category)
        coins = coins.filter(category=category)
    if network_chain != 'all':
        network_chain = NetworkChain.objects.get(slug=network_chain)
        coins = coins.filter(network_chain=network_chain)
    if type_project != 'all':
        type_project = Type.objects.get(slug=type_project)
        coins = coins.filter(type_project=type_project)

    sort_direction = request.GET.get('sort_direction')
    sort_name = request.GET.get('sort_name')

    sort = []
    if sort_name == 'votes' and listing.filter_by == 'best_today':
        sort_name = "votes_today"
    if sort_name == 'votes_today' and listing.filter_by == 'best_all':
        sort_name = "votes"

    if sort_direction == 'asc':
        sort.append(f'-{sort_name}')
    if sort_direction == 'desc':
        sort.append(f'{sort_name}')

    coins = coins.order_by(*sort)

    p = Paginator(coins, 30)
    page_num = request.GET.get('page', 1)
    page = p.page(page_num)

    context = {
        'coins': page,
        "listing": listing,
    }

    pagination = None
    if request.GET.get('is_paginated'):
        pagination = render(request, 'include/pagination.html', context={'page_obj': page}).content.decode("utf-8")

    return JsonResponse({
        'table': render(request, 'include/coin_table.html', context=context).content.decode("utf-8"),
        'pagination': pagination})


def index(request):
    context = {
        'page': Page.objects.get(slug='index'),
        'promoted_listing': Listing.objects.get(slug='promoted'),
        'best_listing': Listing.objects.get(slug='today-s-best'),
    }

    banners = Banner.objects.filter(location__startswith='index', show=True)
    context['banner_under_header'] = banners.filter(location='index_under_header').last()

    total_crypto = [coin for coin in Coin.objects.all()]
    total_trading = [coin.market_cap for coin in total_crypto]
    context['total_trading'] = 0
    for value in total_trading:
        if value:
            context['total_trading'] += value
    context['total_trading'] = get_text_by_number(context['total_trading'])

    total_vote = [coin.votes for coin in total_crypto]
    context['total_votes'] = int(sum(total_vote))
    context['total_currencies'] = len(total_crypto)

    context['new_listing_coin'] = Listing.objects.get(slug="new-listings").get_coins()[:4]
    context['top_today_coin'] = Listing.objects.get(slug="today-s-best").get_coins()[:4]
    context['top_all_time'] = Listing.objects.get(slug="all-time-best").get_coins()[:4]
    context['disable_filter'] = True
    return render(request, 'index.html', context=context)


def vote_coin(request):
    user = request.user
    coin = Coin.objects.get(id=request.GET.get('coin'))

    if not user.is_authenticated:
        return JsonResponse({'status': False})

    if coin not in user.vote_coins.all():
        if user.vote_count <= 0:
            return JsonResponse({'status': False})

        coin.votes += 1
        coin.votes_today += 1
        coin.save()

        user.vote_coins.add(coin)
        user.vote_count -= 1
        if not user.first_vote:
            user.first_vote = timezone.now()
        user.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False})


def advertising(request):
    if request.method == 'POST':
        name = request.POST.get('advertising_name')
        email = request.POST.get('advertising_email')
        question = request.POST.get('advertising_question')

        new_item = AdvertisingItem(name=name, email=email, question=question)
        new_item.save()

    return JsonResponse({"status": "success"})


class Index(TemplateView):
    template_name = 'index.html'
    context_object_name = 'coins'

    def get_context_data(self, *, object_list=None, **kwargs):
        today = timezone.now().date()
        context = super(Index, self).get_context_data(**kwargs)

        context['new_listing_coin'] = Coin.objects.filter(is_moderate=True).order_by('-publish_date')[:4]
        context['top_today_coin'] = Coin.objects.filter(is_moderate=True).annotate(counter_like=Count('vote'),
                                                                                   counter_like_today=Count('vote',
                                                                                                            filter=Q(
                                                                                                                vote__date_new__date=today))).order_by(
            '-counter_like_today')[:4]
        context['top_all_time'] = Coin.objects.filter(is_moderate=True).annotate(counter_like=Count('vote'),
                                                                                 counter_like_today=Count('vote',
                                                                                                          filter=Q(
                                                                                                              vote__date_new__date=today))).order_by(
            '-counter_like')[:4]
        context['coin_counter'] = len(Coin.objects.filter(is_moderate=True))
        context['page'] = Page.objects.get(slug='index')
        context['categories'] = Category.objects.all()
        context['chains'] = NetworkChain.objects.all()
        context['types'] = Type.objects.all()
        total_trading = [coin.market_cap for coin in Coin.objects.all()]
        total_vote = [vote for vote in Vote.objects.all()]
        total_crypto = [coin for coin in Coin.objects.all()]
        total_user = [User for User in User.objects.all()]
        context['total_trading'] = int(sum(total_trading))
        context['total_vote'] = len(total_vote)
        context['total_crypto'] = len(total_crypto)
        context['total_user'] = len(total_user)

        if self.kwargs.get('sort') != 'all_time':
            context['today'] = True
            context['name_filter'] = "Todays's Best"
        else:
            context['all_time'] = True
            context['name_filter'] = 'All Time Best'

        context['socials'] = Social.objects.all()
        context['promoted_coins'] = filter_coins(filter_by='promote')
        context['coins'] = filter_coins(filter_by='best_today')
        return context


class AddCoin(CreateView):
    template_name = 'add-coin.html'
    form_class = CreateCoin
    model = Coin
    success_url = reverse_lazy('core:index')

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'status': 'success'})

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({'status': 'error', 'errors': errors})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AddCoin, self).get_context_data(**kwargs)
        context['page'] = Page.objects.get(slug='add-coin')
        context['categorys'] = Category.objects.all()
        context['listing_platforms'] = ListingPlatform.objects.all()
        context['network_chain'] = NetworkChain.objects.all()
        return context


class CoinDetail(DetailView):
    template_name = 'coin-page.html'
    context_object_name = 'coin'

    def get_queryset(self):
        today = timezone.now().date()
        return Coin.objects.prefetch_related('exchanges__exchange').filter(slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CoinDetail, self).get_context_data(**kwargs)
        context['coins'] = Coin.objects.filter(is_moderate=True, promoted_status=True)[:6]
        context['promoted'] = Listing.objects.get(slug='promoted')
        context['disable_filter'] = True
        increment_metrik(self.request, self.kwargs['slug'])
        return context


class NewlistingList(ListView):
    paginate_by = 6
    template_name = 'new-listing.html'
    model = Coin
    context_object_name = 'coins'

    def get_queryset(self):
        today = timezone.now().date()
        filter_by = self.kwargs.get('filter_by')
        coins = filter_coins(filter_by)

        if not coins:
            sort = self.kwargs.get('sort')
            sort_item = self.kwargs.get('sort_item')
            sort_status = self.kwargs.get('sort_status')
            return get_sorted_mixin(sort_item, sort_status, sort)
        return coins

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewlistingList, self).get_context_data(**kwargs)
        context['page'] = Page.objects.get(slug='coin-list')
        context['sort_item'] = self.request.path.split('/')[-1]
        context['sort_item_2'] = self.request.path.split('/')[-2]
        context['categories'] = Category.objects.all()
        context['chains'] = NetworkChain.objects.all()
        context['types'] = Type.objects.all()
        context['name_filter'] = 'New Listings'

        filter_by = self.kwargs.get('filter_by')
        if self.kwargs.get('sort_item'):
            context['del_block'] = True

        if filter_by == 'promote':
            context['name_filter'] = 'Promoted'
            context['if_promote'] = True
        if filter_by == 'new_listing':
            context['name_filter'] = 'New Listings'
            context['del_block'] = True
        elif filter_by == 'best_all_time':
            context['name_filter'] = 'All Time Best'
            context['all_time'] = True
        elif filter_by == 'all_time_best':
            context['name_filter'] = 'All Time Best'
            context['all_time'] = True
        elif filter_by == 'best_today':
            context['name_filter'] = "Todays's Best"
            context['today'] = True
        elif filter_by == 'all':
            context['name_filter'] = 'All Coin'
        else:
            context['name_filter'] = ''
        return context


class NewlistingListCategory(ListView):
    paginate_by = 6
    template_name = 'new-listing.html'
    model = Coin
    context_object_name = 'coins'

    def get_queryset(self):
        sort = self.kwargs.get('sort')
        sort_item = self.kwargs.get('sort_item')
        sort_status = self.kwargs.get('sort_status')
        filter_name = self.kwargs.get('slug')
        return get_sorted_mixin(sort_item=sort_item, sort_status=sort_status, sort=sort, type_filter='category',
                                filter_name=filter_name)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewlistingListCategory, self).get_context_data(**kwargs)
        context['page'] = Page.objects.get(slug='coin-list')
        context['sort_item'] = self.request.path.split('/')[-1]
        context['sort_item_2'] = self.request.path.split('/')[-2]
        context['categories'] = Category.objects.all()
        context['chains'] = NetworkChain.objects.all()
        context['types'] = Type.objects.all()
        if self.kwargs.get('sort_item'):
            context['del_block'] = True
        return context


class NewlistingListPromote(ListView):
    paginate_by = 6
    template_name = 'promoted-list.html'
    model = Coin
    context_object_name = 'coins'

    def get_queryset(self):
        sort_item = self.kwargs.get('sort_item')
        sort_status = self.kwargs.get('sort_status')
        return get_sorted_mixin(sort_item=sort_item, sort_status=sort_status, is_promoted=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewlistingListPromote, self).get_context_data(**kwargs)
        context['page'] = Page.objects.get(slug='coin-list')
        context['sort_item'] = self.request.path.split('/')[-1]
        context['sort_item_2'] = self.request.path.split('/')[-2]
        context['categories'] = Category.objects.all()
        context['chains'] = NetworkChain.objects.all()
        context['types'] = Type.objects.all()
        context['if_promote'] = True
        if self.kwargs.get('sort_item'):
            context['del_block'] = True
        return context


class NewlistingListChain(ListView):
    paginate_by = 6
    template_name = 'new-listing.html'
    model = Coin
    context_object_name = 'coins'

    def get_queryset(self):
        sort = self.kwargs.get('sort')
        sort_item = self.kwargs.get('sort_item')
        sort_status = self.kwargs.get('sort_status')
        filter_name = self.kwargs.get('slug')
        type_filter = 'network_chain'
        return get_sorted_mixin(sort_item=sort_item, sort_status=sort_status, sort=sort, type_filter=type_filter,
                                filter_name=filter_name)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewlistingListChain, self).get_context_data(**kwargs)
        context['page'] = Page.objects.get(slug='coin-list')
        context['sort_item'] = self.request.path.split('/')[-1]
        context['sort_item_2'] = self.request.path.split('/')[-2]
        context['categories'] = Category.objects.all()
        context['chains'] = NetworkChain.objects.all()
        context['types'] = Type.objects.all()
        if self.kwargs.get('sort_item'):
            context['del_block'] = True
        return context


class NewlistingListType(ListView):
    template_name = 'new-listing.html'
    model = Coin
    context_object_name = 'coins'

    def get_queryset(self):
        sort = self.kwargs.get('sort')
        sort_item = self.kwargs.get('sort_item')
        sort_status = self.kwargs.get('sort_status')
        filter_name = self.kwargs.get('slug')
        type_filter = 'type_project'
        return get_sorted_mixin(sort_item=sort_item, sort_status=sort_status, sort=sort, type_filter=type_filter,
                                filter_name=filter_name)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewlistingListType, self).get_context_data(**kwargs)
        context['page'] = Page.objects.get(slug='coin-list')
        context['sort_item'] = self.request.path.split('/')[-1]
        context['sort_item_2'] = self.request.path.split('/')[-2]
        context['categories'] = Category.objects.all()
        context['chains'] = NetworkChain.objects.all()
        context['types'] = Type.objects.all()
        if self.kwargs.get('sort_item'):
            context['del_block'] = True
        return context


class PrivacyPolice(TemplateView):
    template_name = 'privacy-police.html'
    model = Page

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PrivacyPolice, self).get_context_data(**kwargs)
        context['page'] = Page.objects.get(slug='privacy-police')
        return context


class SearchList(ListView):
    template_name = 'new-listing.html'
    context_object_name = 'coins'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            results = Coin.objects.filter(coin_name__icontains=query, is_moderate=True).annotate(
                counter_like=Count('votes'))
        else:
            results = []
        return results

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchList, self).get_context_data(**kwargs)
        context['page'] = Page.objects.get(slug='search')
        context['listing'] = Listing.objects.get(slug='new-listings')
        return context


def captcha_view(request):
    if request.method == 'POST':
        coin_pk = request.POST.get('coin_pk')
        form = CaptchaForm(request.POST)
        if form.is_valid():
            return increment_counter(request, coin_pk)
    return redirect('core:index')


def get_sort_status_promoted(request):
    if request.method == 'GET':
        previous_page = request.GET.get('previous_page')[4:]
        sort_name = request.GET.get('sort_name')

        if previous_page == f'index/{sort_name}/asc/':
            return redirect('core:index_sorted_item', sort_name, 'desc')
        elif previous_page == f'index/{sort_name}/desc/':
            return redirect('core:index_sorted_item', sort_name, 'asc')
        else:
            return redirect('core:index_sorted_item', sort_name, 'asc')


def get_sort_status_list(request):
    if request.method == 'GET':
        previous_page = request.GET.get('previous_page')[4:]
        sort_name = request.GET.get('sort_name')
        previous_page_type = str(previous_page).split('/')[0]
        if str(previous_page).split('/')[-1]:
            previous_page_name = str(previous_page).split('/')[-1]
        else:
            previous_page_name = str(previous_page).split('/')[1]

        if previous_page_type == 'coin-list':
            if previous_page == f'coin-list/{sort_name}/asc/':
                return redirect('core:list_sorted_item', sort_name, 'desc')
            elif previous_page == f'coin-list/{sort_name}/desc/':
                return redirect('core:list_sorted_item', sort_name, 'asc')
            else:
                return redirect('core:list_sorted_item', sort_name, 'asc')

        elif previous_page_type == 'coin-category':
            if previous_page == f'coin-category/{sort_name}/asc/{previous_page_name}':
                return redirect('core:category_sorted_item', sort_name, 'desc', previous_page_name)
            elif previous_page == f'coin-category/{sort_name}/desc/{previous_page_name}':
                return redirect('core:category_sorted_item', sort_name, 'asc', previous_page_name)
            else:
                return redirect('core:category_sorted_item', sort_name, 'asc', previous_page_name)

        elif previous_page_type == 'coin-chain':
            if previous_page == f'coin-chain/{sort_name}/asc/{previous_page_name}':
                return redirect('core:chain_sorted_item', sort_name, 'desc', previous_page_name)
            elif previous_page == f'coin-chain/{sort_name}/desc/{previous_page_name}':
                return redirect('core:chain_sorted_item', sort_name, 'asc', previous_page_name)
            else:
                return redirect('core:chain_sorted_item', sort_name, 'asc', previous_page_name)

        elif previous_page_type == 'coin-type':
            if previous_page == f'coin-type/{sort_name}/asc/{previous_page_name}':
                return redirect('core:type_sorted_item', sort_name, 'desc', previous_page_name)
            elif previous_page == f'coin-chain/{sort_name}/desc/{previous_page_name}':
                return redirect('core:type_sorted_item', sort_name, 'asc', previous_page_name)
            else:
                return redirect('core:type_sorted_item', sort_name, 'asc', previous_page_name)


def get_sort_status_profile(request):
    if request.method == 'GET':
        previous_page = request.GET.get('previous_page')[4:]
        sort_name = request.GET.get('sort_name')
        user_pk = request.user.pk

        if previous_page == f'account-liked/{user_pk}/{sort_name}/asc/':
            return redirect('user:account-liked-sort', user_pk, sort_name, 'desc')
        elif previous_page == f'account-liked/{sort_name}/desc/':
            return redirect('user:account-liked-sort', user_pk, sort_name, 'asc')
        else:
            return redirect('user:account-liked-sort', user_pk, sort_name, 'asc')


def get_sort_status_promote(request):
    if request.method == 'GET':
        previous_page = request.GET.get('previous_page')[4:]
        sort_name = request.GET.get('sort_name')

        if previous_page == f'coin-promoted/{sort_name}/asc/':
            return redirect('core:promote-sort', sort_name, 'desc')
        elif previous_page == f'coin-promoted/{sort_name}/desc/':
            return redirect('core:promote-sort', sort_name, 'asc')
        else:
            return redirect('core:promote-sort', sort_name, 'asc')


def get_sorted_mixin(sort_item, sort_status, sort=None, is_promoted: bool = None, profile=None, type_filter=None,
                     filter_name=None):
    return Coin.objects.filter(is_moderate=True)
    today = timezone.now().date()

    if sort_item:
        if sort_status == 'asc':
            coin = Coin.objects.filter(is_moderate=True).annotate(counter_like=Count('vote'),
                                                                  counter_like_today=Count('vote', filter=Q(
                                                                      vote__date_new__date=today))).order_by(sort_item)
        else:
            coin = Coin.objects.filter(is_moderate=True).annotate(counter_like=Count('vote'),
                                                                  counter_like_today=Count('vote', filter=Q(
                                                                      vote__date_new__date=today))).order_by(
                '-' + sort_item)

        if is_promoted:
            coin = coin.filter(promoted_status=True)

        if type_filter == 'network_chain':
            coin = coin.filter(network_chain__slug=filter_name)
        elif type_filter == 'category':
            coin = coin.filter(category__slug=filter_name)
        elif type_filter == 'type_project':
            coin = coin.filter(type_project__slug=filter_name)

        if profile:
            coin = coin.filter(favorite=profile)
        return coin

    if sort == 'all_time':
        coin = Coin.objects.filter(is_moderate=True).annotate(counter_like=Count('vote'),
                                                              counter_like_today=Count('vote', filter=Q(
                                                                  vote__date_new__date=today))).order_by(
            '-counter_like')
    else:
        coin = Coin.objects.filter(is_moderate=True).annotate(counter_like=Count('vote'),
                                                              counter_like_today=Count('vote', filter=Q(
                                                                  vote__date_new__date=today))).order_by(
            '-counter_like')

    if is_promoted:
        coin = coin.filter(promoted_status=True)

    if type_filter == 'network_chain':
        coin = coin.filter(network_chain__slug=filter_name)
    elif type_filter == 'category':
        coin = coin.filter(category__slug=filter_name)
    elif type_filter == 'type_project':
        coin = coin.filter(type_project__slug=filter_name)

    if profile:
        coin = coin.filter(favorite=profile)
    return coin


def coin_price_history(request):
    coin_id = request.GET.get('coinId')
    api_type = request.GET.get('type')
    period = request.GET.get('period')

    if api_type == 'coinranking':
        url = f'https://api.coinranking.com/v2/coin/{coin_id}/history'
        params = {'timePeriod': period}
        headers = {'x-access-token': os.getenv('COINRANKING_API_KEY')}

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return JsonResponse(response.json(), safe=False)
        else:
            return JsonResponse({'error': 'Failed to retrieve data from CoinRanking'}, status=500)

    elif api_type == 'uniswap':
        days = convert_period_to_days(period)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())
        if period == '24h':
            interval = 'hour'
            query = '''
                {
                    tokenHourDatas(where: { token: "%s", periodStartUnix_gte: %d, periodStartUnix_lte: %d }, orderBy: periodStartUnix, orderDirection: desc) {
                        priceUSD
                        periodStartUnix
                    }
                }
                ''' % (coin_id, start_timestamp, end_timestamp)
        elif period == '7d':
            interval = '12h'
            query = '''
                {
                    tokenHourDatas(where: { token: "%s", periodStartUnix_gte: %d, periodStartUnix_lte: %d }, orderBy: periodStartUnix, orderDirection: desc) {
                        priceUSD
                        periodStartUnix
                    }
                }
                ''' % (coin_id, start_timestamp, end_timestamp)
        else:
            interval = 'day'
            query = '''
                {
                    tokenDayDatas(where: { token: "%s", date_gte: %d, date_lte: %d }, orderBy: date, orderDirection: desc) {
                        priceUSD
                        date
                    }
                }
                ''' % (coin_id, start_timestamp, end_timestamp)
        url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'
        response = requests.post(url, json={'query': query})
        if response.status_code == 200:
            data = response.json()
            if period == '24h' or period == '7d':
                history = [
                    {
                        'price': item['priceUSD'],

                        'timestamp': item['periodStartUnix']
                    }
                    for item in data['data']['tokenHourDatas']
                ]
            else:
                history = [
                    {
                        'price': item['priceUSD'],
                        'timestamp': item['date']
                    }
                    for item in data['data']['tokenDayDatas']
                ]
            result = {
                'status': 'success',
                'data': {
                    'change': None,
                    'history': history
                }
            }
            return JsonResponse(result, safe=False)
        else:
            return JsonResponse({'error': 'Failed to retrieve data from Uniswap'}, status=500)
    else:
        return JsonResponse({'error': 'Unsupported API type'}, status=400)
