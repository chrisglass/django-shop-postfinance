#-*- coding: utf-8 -*-
'''
Let's have the same approach than django-paypal, it's pretty convenient.

We'll build a form that we can then render in the views, so we don't have
to spit out this pesky boilerplate ever again.

'''
from django import forms

class ValueHiddenInput(forms.HiddenInput):
    """
    Widget that renders only if it has a value.
    Used to remove unused fields from Postfinance buttons.
    
    This is a 1 to 1 compy of the excellent widget by django-paypal author.
    Original can be found at:
    
    https://github.com/johnboxall/django-paypal/blob/master/standard/widgets.py
    
    """
    def render(self, name, value, attrs=None):
        if value is None:
            return u''
        else:
            return super(ValueHiddenInput, self).render(name, value, attrs)

class PostfinanceForm(forms.Form):
    '''
                    <!-- general parameters: see chapter 5.2 -->
                <input type="hidden" name="PSPID" value="divioTEST">
                
                <input type="hidden" name="orderID" value="{{order.id|test_prefix}}">
                <input type="hidden" name="amount" value="{{ order.total|smallest_monetary_unit }}">
                <!--<input type="hidden" name="TP" value="http://127.0.0.1:8000/shop/template">-->
                <input type="hidden" name="bgcolor" value="#FFFFFF">
                <input type="hidden" name="currency" value="CHF">
                <input type="hidden" name="language" value="de_DE">
                {% with order.id|test_prefix as theid %}
                <input type="hidden" name="SHASign" value="{% sha1 order.total 'CHF' 'de_DE' theid 'divioTEST' %}">
    '''
    PSPID = forms.CharField(widget=ValueHiddenInput())
    orderID = forms.CharField(widget=ValueHiddenInput())
    amount = forms.CharField(widget=ValueHiddenInput())
    bgcolor = forms.CharField(widget=ValueHiddenInput()) # That should really be a color!
    currency = forms.CharField(widget=ValueHiddenInput())
    language = forms.CharField(widget=ValueHiddenInput())
    SHASign = forms.CharField(widget=ValueHiddenInput())