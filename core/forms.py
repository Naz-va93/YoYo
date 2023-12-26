from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox
from django.forms import ModelForm
from django import forms
from core.models import *


class CreateCoin(ModelForm):
    class Meta:
        model = Coin
        fields = "__all__"
        exclude = ['votes', 'votes_today', 'website_url']


class AddItem(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['date', 'coin', 'type']


class OrderForm(ModelForm):
    class Meta:
        model = CreateOrder
        fields = "__all__"


class CaptchaForm(forms.Form):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            attrs={'theme': 'dark'}
        )
    )
    coin_pk = forms.IntegerField()


class SortForm(forms.Form):
    sort = forms.CharField()