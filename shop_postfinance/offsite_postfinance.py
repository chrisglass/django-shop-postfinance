from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render_to_response
from shop_postfinance.utils import security_check


class OffsitePostfinanceBackend(object):
    backend_name = "Postfinance"
    url_namespace = "postfinance"
    
    #===========================================================================
    # Defined by the backends API
    #===========================================================================
    
    def __init__(self, shop):
        self.shop = shop
        assert settings.POSTFINANCE_SECRET_KEY, 'You need to define a POSTFINANCE_SECRET_KEY="..." setting in your settings file.'
        
    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^$', self.view_that_asks_for_money, name='postfinance' ),
            url(r'^success$', self.paypal_successful_return_view, name='paypal_success' ),
            url(r'^/somethinghardtoguess/instantpaymentnotification/$', include('paypal.standard.ipn.urls')),
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
        #TODO: Do the postfinance dance here. 
        
        # Create the instance.
        #form = PayPalPaymentsForm(initial=paypal_dict)
        #context = {"form": form}
        context = {}
        return render_to_response("payment.html", context)
    
    
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
            
            # TODO: Save order details in the database (with a postfinance model)
            
            order_id = data['orderID']
            order = self.shop.get_order_for_id(order_id) # Get the order from either the POST or the GET parameters
            transaction_id = data['PAYID']
            amount = data['amount']
            # This actually records the payment in the shop's database
            self.shop.confirm_payment(order, amount, transaction_id, self.backend_name)
            
            return HttpResponse('OKAY')
            
        else: # Checksum failed
            return HttpResponseBadRequest()