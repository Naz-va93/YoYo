from django.urls import path

from user.utils import increment_favorite
from user.views import ProfileUser, LikedCoin

app_name = 'user'


urlpatterns = [
    path('profile/<int:pk>/', ProfileUser.as_view(), name='profile'),
    path('account-liked/<int:pk>/', LikedCoin.as_view(), name='account-liked'),
    path('increment_favorite/<int:pk>/', increment_favorite, name='add_favorite'),

    path('account-liked/<int:pk>/<str:sort_item>/<str:sort_status>/', LikedCoin.as_view(), name='account-liked-sort'),

]
