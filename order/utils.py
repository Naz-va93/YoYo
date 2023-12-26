from decimal import Decimal

from django.shortcuts import redirect

from core.models import Coin, OrderItem, Cart, CreateOrder, CartCold


class CartUtils:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, pk, date, type):
        if date not in self.cart:
            self.cart[date] = [pk]
        else:
            self.cart[date].append(pk)
        self.save()

    def remove(self, slug):
        if str(slug) in self.cart:
            del self.cart[str(slug)]
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Coin.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['total_price'] = item['product'].price * item['quantity']
            yield item

    def get_total_price(self):
        total_price = 0
        for key, value in self.request.session['cart']:
            coin = Coin.objects.get(pk=key)
            price = coin.price_for_promote
            total_price = Decimal(price) * Decimal(len(value))
        return total_price

    def create_info_in_db(self):
        cart = CartCold.objects.create()
        for key, value in self.session['cart'].items():
            try:
                coin = Coin.objects.get(pk=key)
                sum = Decimal(coin.price_for_promote) * Decimal(len(value[0]))
                OrderItem.objects.create(coin=coin, cart_cold=cart, type='Promote Spot', date=value[0], sum=sum)
            except:
                sum = Decimal(0.15)
                OrderItem.objects.create(cart_cold=cart, type='Banner', date=value[0], sum=sum)
        cart.update_total_sum()
        print(cart.pk, 12121212212112121)
        return cart.pk


def add_item(request, data):
    user = request.user
    try:
        coin = Coin.objects.get(pk=data['coin'])
    except:
        coin = None
    if user.is_authenticated:
        cart = Cart.objects.get(user=user.pk)
        if cart:
            if coin:
                order = OrderItem.objects.create(coin=coin, type='Promote coin', cart=cart, date=data['date'])
                order.update_sum(order.pk)
                cart.update_total_sum()
                return redirect('order:promote')
            else:
                order = OrderItem.objects.create(type='Banner', photo=data['photo'], url=data['url'], cart=cart,
                                                 date=data['date'])
                order.sum = 0
                if cart.total_sum:
                    cart.total_sum = Decimal(cart.total_sum)
                    cart.total_sum += Decimal(len(data['date'])) * Decimal('0.15')
                    round(cart.total_sum)
                else:
                    cart.total_sum = Decimal('0')
                    cart.total_sum += Decimal('0.15')
                    round(cart.total_sum)
                order.sum += Decimal(len(data['date'])) * Decimal('0.15')
                round(order.sum)
                cart.save()
                order.save()
                return redirect('order:promote')
        else:
            cart = Cart.objects.create(user=user)
            OrderItem.objects.create(coin=coin, type=data['type'], cart=cart, date=data['date'])
            return redirect('order:promote')

    if coin:
        CartUtils(request).add(data['date'], data['coin'], data['type'])
    else:
        CartUtils(request).add(data['date'], data['type'], data['type'])
    return redirect('order:promote')


def remove_item(request, pk):
    user = request.user

    if user.is_authenticated:
        cart = Cart.objects.get(user=user.pk)
        if cart:
            OrderItem.objects.get(pk=pk).delete()
            cart.update_total_sum()
            return redirect('order:promote')
    else:
        CartUtils(request).remove(pk)
        return redirect('order:promote')


def remove_item_slug(request, slug):
    CartUtils(request).remove(slug)
    return redirect('order:promote')
