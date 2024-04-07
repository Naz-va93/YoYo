from django.db.models import Count, Q
from django.http import Http404
from django.views.generic import ListView

from core.models import Page, OrderItem, Cart, Coin, CreateOrder, CartCold, Listing, Order
from core.views import get_sorted_mixin


class ProfileUser(ListView):
    template_name = 'account-profile.html'

    def get_queryset(self):
        return OrderItem.objects.filter(cart__user=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProfileUser, self).get_context_data(**kwargs)
        context['page'] = Page.objects.get(slug='profile')
        context['orders'] = Order.objects.filter(user__pk=self.kwargs['pk']).select_related('coin')
        return context


class LikedCoin(ListView):
    paginate_by = 6
    template_name = 'account-liked-coins.html'
    model = Page

    # def get_queryset(self):
    #     sort = self.kwargs.get('sort')
    #     sort_item = self.kwargs.get('sort_item')
    #     sort_status = self.kwargs.get('sort_status')
    #     user = self.request.user
    #     if user.is_authenticated and (user.pk == self.kwargs['pk']):
    #         return get_sorted_mixin(sort_item, sort_status, sort, profile=True)
    #     raise Http404

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LikedCoin, self).get_context_data(**kwargs)
        context['page'] = Page.objects.get(slug='like-coin')
        context['listing'] = Listing.objects.get(slug='all-coins')
        context['coins'] = context['listing'].get_coins().filter(favorite__in=[self.request.user])
        context['is_profile'] = True
        return context
