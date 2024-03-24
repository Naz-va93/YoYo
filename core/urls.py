from django.contrib import admin
from django.urls import path

from core import views
from core.views import *
from core.utils import *

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('index/<str:sort>/', Index.as_view(), name='index_sorted'),

    path('index/<str:sort_item>/<str:sort_status>/', Index.as_view(), name='index_sorted_item'),
    path('coin-list/<slug>/', coin_list, name='list_sorted_item'),
    path('vote-coin/', vote_coin, name='vote_coin'),

    path('advertising/', advertising, name='advertising'),

    path('add-coin/', AddCoin.as_view(), name='add-coin'),
    path('coin-page/<slug:slug>/', CoinDetail.as_view(), name='coin-page'),
    path('coin-list/<str:filter_by>/', NewlistingList.as_view(), name='coin-list'),
    path('page/<slug>/', page, name='page'),
    path('search/', SearchList.as_view(), name='search'),
    path('coin-category/<slug:slug>/', NewlistingListCategory.as_view(), name='coin-list-category'),
    path('coin-category/<str:sort_item>/<str:sort_status>/<str:slug>', NewlistingListCategory.as_view(), name='category_sorted_item'),
    path('coin-chain/<slug:slug>/', NewlistingListChain.as_view(), name='coin-list-chain'),
    path('coin-chain/<str:sort_item>/<str:sort_status>/<str:slug>', NewlistingListChain.as_view(), name='chain_sorted_item'),
    path('coin-type/<slug:slug>/', NewlistingListType.as_view(), name='coin-list-type'),
    path('coin-type/<str:sort_item>/<str:sort_status>/<str:slug>', NewlistingListType.as_view(), name='type_sorted_item'),
    path('custom_set_language/', custom_set_language, name='custom_set_language'),
    path('add_like/<int:pk>/', increment_counter, name='add_like'),

    path('coin-promoted/', NewlistingListPromote.as_view(), name='promote-coin'),
    path('coin-promoted/<str:sort_item>/<str:sort_status>/', NewlistingListPromote.as_view(), name='promote-sort'),

    path('captcha/', captcha_view, name='captcha'),
    path('sort/', get_sort_status_promoted, name='sort'),
    path('sort-promote/', get_sort_status_promote, name='sort-promote'),
    path('sort-list/', get_sort_status_list, name='sort-list'),
    path('sort-profile/', get_sort_status_profile, name='sort-profile'),

    path('search-ajax/', search_coins_ajax, name='search_ajax'),
    path('sort-ajax/', sort_filter_pagination_ajax, name='sort_ajax'),
    path('get_coins_table/', get_coins_table, name='get_coins_table'),

]
