from decimal import Decimal

from django.db.models import Count
from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView
from core.forms import OrderForm, AddItem
from core.models import Coin, Page, OrderItem, Cart, CreateOrder, CartCold
from order.utils import CartUtils, add_item


class OrderLookUpOrDone(DetailView):
    template_name = 'order-lookup.html'
    context_object_name = 'order'

    def get_queryset(self):
        return CreateOrder.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderLookUpOrDone, self).get_context_data(**kwargs)
        order = CreateOrder.objects.get(pk=self.kwargs['pk'])
        context['page'] = Page.objects.get(slug='order-look')
        context['coins'] = Coin.objects.filter(is_moderate=True)
        try:
            context['cart'] = CartCold.objects.get(pk=order.cart_cold.pk)
        except:
            context['cart'] = ''
        try:
            context['items'] = OrderItem.objects.filter(cart_cold=order.cart_cold.pk)
        except:
            context['items'] = ''
        return context


class Promote(TemplateView):
    template_name = 'promote.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Promote, self).get_context_data(**kwargs)
        context['page'] = Page.objects.get(slug='promote')
        context['coins'] = Coin.objects.filter(is_moderate=True)
        if self.request.user.is_authenticated:
            try:
                context['items_in_order'] = OrderItem.objects.filter(cart__user=self.request.user)
            except:
                context['items_in_order'] = ''
            try:
                context['cart'] = Cart.objects.get(user=self.request.user.pk)
            except:
                context['cart'] = Cart.objects.create(user=self.request.user)
        else:
            try:
                sum = 0
                context['items_in_order'] = self.request.session['cart']
                for key, value in self.request.session['cart'].items():
                    try:
                        for val in value:
                            coin = Coin.objects.get(pk=key)
                            sum += Decimal(coin.price_for_promote) * Decimal(len(val))
                    except:
                        for val in value:
                            sum += Decimal('0.15') * Decimal(len(val))
                context['total_sum'] = str(sum)[:5]
            except:
                context['items_in_order'] = ''
        return context

    def post(self, request, *args, **kwargs):
        first_form = request.POST.copy()
        second_form = OrderForm(request.POST)
        date_strings = request.POST.getlist('date')
        date_values = ['-'.join(date.split('-')[::-1]) for date in date_strings]
        form_1 = AddItem(first_form)
        form_1.data['date'] = date_values

        if second_form.is_valid():
            if not self.request.user.is_authenticated:
                cart_cold = CartCold.objects.get(pk=CartUtils(self.request).create_info_in_db())
                instance = second_form.save()
                instance.cart_cold = cart_cold
                instance.save()
                del self.request.session['cart']
                return redirect('order:order-lookup', pk=instance.id)
            else:
                instance = second_form.save()
                instance.user = self.request.user
                cart = Cart.objects.get(user=self.request.user.pk)
                cart_cold = CartCold.objects.create(user=self.request.user, total_sum=cart.total_sum, live_cart=cart.pk)
                instance.cart_cold = cart_cold
                instance.save()
                for item in OrderItem.objects.filter(cart=cart):
                    item.cart_cold = cart_cold
                    item.save()
                cart.delete()

                if self.request.user.is_authenticated:
                    return redirect('order:order-lookup', pk=instance.id)
                else:
                    return redirect('order:order-lookup', pk=instance.id)

        if form_1.is_valid():
            add_item(request, form_1.data)
            return redirect('order:promote')
        return redirect('order:promote')
