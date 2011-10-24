from django import forms
from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
from django.forms.forms import DeclarativeFieldsMetaclass
from django.http import (HttpResponseBadRequest, HttpResponse, 
    HttpResponseRedirect)
from django.shortcuts import render_to_response
from django.utils.translation import get_language
from shop_postfinance.forms import ValueHiddenInput
from shop_postfinance.models import PostfinanceIPN
from shop_postfinance.utils import security_check, compute_security_checksum


def absolute_url(request, path):
    return '%s://%s%s' % ('https' if request.is_secure() else 'http', 
                          request.get_host(), path)


class OffsitePostfinanceBackend(object):
    backend_name = "Postfinance"
    url_namespace = "postfinance"
    
    #===========================================================================
    # Defined by the backends API
    #===========================================================================
    
    def __init__(self, shop):
        self.shop = shop
        assert getattr(settings, 'POSTFINANCE_SECRET_KEY', None), 'You need to define a POSTFINANCE_SECRET_KEY="..." setting in your settings file.'
        assert getattr(settings, 'POSTFINANCE_PSP_ID', None), 'Please define a POSTFINANCE_PSP_ID="..." setting in your settings file.'
        assert getattr(settings, 'POSTFINANCE_CURRENCY', None), 'Please define a POSTFINANCE_CURRENCY="..." setting in your settings file.'
        self.extra_data = getattr(settings, 'POSTFINANCE_EXTRA_CONFIGS', {})
        self.language_conversion_table = getattr(settings, 'POSTFINANCE_RFC5646_CONVERSION_TABLE', {})
        self.fallback_language = getattr(settings, 'POSTFINANCE_FALLBACK_LANGUAGE', None)
        if self.fallback_language:
            # validate
            errmsg = ('POSTFINANCE_FALLBACK_LANGUAGE setting must be in '
                'format "xx_YY" where "xx" is a ISO-639-1 code and "YY" a '
                'ISO-3166 code.')
            assert self.fallback_language.count('_') == 1, errmsg
            assert len(self.fallback_language) == 5, errmsg
            assert self.fallback_language[0].islower(), errmsg
            assert self.fallback_language[1].islower(), errmsg
            assert self.fallback_language[2] == '_'
            assert self.fallback_language[3].isupper(), errmsg
            assert self.fallback_language[4].isupper(), errmsg
        else:
            self.fallback_language = 'de_DE'
    
    def _convert_language(self, rfc5646_language_code):
        """
        Turn a RFC5646 (http://tools.ietf.org/html/rfc5646) language code into
        ISO-639-1+ISO-3166 language codes using the
        POSTFINANCE_RFC5646_CONVERSION_TABLE setting or returns the fallback
        as defined in POSTFINANCE_FALLBACK_LANGUAGE (or 'de_DE' if None is
        defined).
        """
        found = self.language_conversion_table.get(rfc5646_language_code)
        if found:
            return found
        return self.fallback_language

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^$', self.view_that_asks_for_money, name='postfinance' ),
            url(r'^success/$', self.postfinance_return_successful_view, name='postfinance_success' ),
            url(r'^somethinghardtoguess/instantpaymentnotification/$', self.postfinance_ipn, 'postfinance_ipn'),
        )
        return urlpatterns
    
    #===========================================================================
    # Views
    #===========================================================================
    
    def view_that_asks_for_money(self, request):
        '''
        We need this to be a method and not a function, since we need to have
        a reference to the shop interface
        '''
        order = self.shop.get_order(request)
        order_id = self.shop.get_order_unique_id(order)
        amount = self.shop.get_order_total(order)
        currency = settings.POSTFINANCE_CURRENCY.upper()
        language = self._convert_language(get_language())
        
        amount = str(int(amount * 100))
        
        postfinance_dict = {
            'PSPID': settings.POSTFINANCE_PSP_ID ,
            'orderID': order_id,
            'amount': amount,
            'currency': currency,
            'language': language,
            'ACCEPTURL': absolute_url(request, reverse('postfinance_success')),
            'CANCELURL': absolute_url(request, reverse('cart_delete')),
        }
        postfinance_dict.update(self.extra_data)
        postfinance_dict['SHASign'] = compute_security_checksum(**postfinance_dict)
        
        fields = {}
        for key in postfinance_dict:
            fields[key] = forms.CharField(widget=ValueHiddenInput())
        
        form_class = DeclarativeFieldsMetaclass('PostfinanceForm', (forms.Form,), fields)
        form = form_class(initial=postfinance_dict)
        context = {'form': form}
        return render_to_response("payment.html", context)
    
    def postfinance_return_successful_view(self, request):
        return HttpResponseRedirect(self.shop.get_finished_url())
    
    def postfinance_ipn(self, request):
        """
        Similar to paypal's IPN, postfinance will send an instant notification to the website, 
        passing the following parameters in the URL:
        
        orderID=Test27&
        currency=CHF&
        amount=54&
        PM=CreditCard&
        ACCEPTANCE=test123&
        STATUS=9&
        CARDNO=XXXXXXXXXXXX3333&ED=0317&
        CN=Testauzore+Testos&
        TRXDATE=11/08/10&
        PAYID=8628366&
        NCERROR=0&
        BRAND=VISA&
        IPCTY=CH&
        CCCTY=US&
        ECI=7&
        CVCCheck=NO&
        AAVCheck=NO&
        VC=NO&
        IP=84.226.127.220&
        SHASIGN=CEE483B0557B8E3437A55094221E15C7DB6A0D63
        
        Cornfirms that payment has been completed and marks invoice as paid.
        This can come from two sources: Wither the client was redirected to our success page from postfinance (and so the order
        information is contained in GET parameters), or the client messed up and postfinance sends us a direct server-to-server
        http connection with parameters passed in the POST fields.
        
        """
        
        data = request.REQUEST
        # Verify that the info is valid (with the SHA sum)
        valid = security_check(data, settings.POSTFINANCE_SECRET_KEY)
        if valid:
            order_id = data['orderID']
            order = self.shop.get_order_for_id(order_id) # Get the order from either the POST or the GET parameters
            transaction_id = data['PAYID']
            amount = data['amount']
            # Create an IPN transaction trace in the database
            PostfinanceIPN.objects.create(
                orderID=order_id,
                currency=order.get('currency', ''),
                amount=order.get('amount', ''),
                PM=order.get('PM', ''),
                ACCEPTANCE=order.get('ACCEPTANCE', ''),
                STATUS=order.get('STATUS', ''),
                CARDNO=order.get('CARDNO', ''),
                CN=order.get('CN', ''),
                TRXDATE=order.get('TRXDATE', ''),
                PAYID=order.get('PAYID', ''),
                NCERROR=order.get('NCERROR', ''),
                BRAND=order.get('BRAND', ''),
                IPCTY=order.get('IPCTY', ''),
                CCCTY=order.get('CCCTY', ''),
                ECI=order.get('ECI', ''),
                CVCCheck=order.get('CVCCheck', ''),
                AAVCheck=order.get('AAVCheck', ''),
                VC=order.get('VC', ''),
                IP=order.get('IP', ''),
                SHASIGNorder =order.get('SHASIGNorder', ''),
            )
            # This actually records the payment in the shop's database
            self.shop.confirm_payment(order, amount, transaction_id, self.backend_name)
            
            return HttpResponse('OKAY')
            
        else: # Checksum failed
            return HttpResponseBadRequest()
