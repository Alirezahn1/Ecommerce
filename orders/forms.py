
from django import forms


class CartAddForm(forms.Form):
    amount = forms.IntegerField(min_value=1)