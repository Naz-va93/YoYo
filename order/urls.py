from django.urls import path

from core.views import *
from core.utils import *
from order.utils import add_item, remove_item, remove_item_slug
from order.views import OrderLookUpOrDone, Promote


app_name = 'order'


urlpatterns = [
    path('order-lookup/<int:pk>', OrderLookUpOrDone.as_view(), name='order-lookup'),
    # path('promote/', Promote.as_view(), name='promote'),
    #
    # path('add_item/', add_item, name='add_item'),
    # path('remove_item/<int:pk>', remove_item, name='remove_item'),
    # path('remove_item_slug/<slug:slug>', remove_item_slug, name='remove_item_slug'),

]
