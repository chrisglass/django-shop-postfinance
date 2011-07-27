from django.db import models


class PostfinanceIPN(models.Model):
    """
    A simple, dumb model that traces all the IPNs recieved from postfinance,
    for archiving reasons.
    
    This isn't really human friends, but should still be kept in the database
    for a while (most probably 10years if you're in Switzerland, since this is
    an accounting piece.
    
    I am not a lawyer :)
    """
    orderID = models.CharField(max_length=255)#=Test27&
    currency = models.CharField(max_length=255)#=CHF&
    amount = models.CharField(max_length=255) #=54&
    PM = models.CharField(max_length=255) #=CreditCard&
    ACCEPTANCE = models.CharField(max_length=255) #=test123&
    STATUS = models.CharField(max_length=255) #=9&
    CARDNO = models.CharField(max_length=255) #=XXXXXXXXXXXX3333&ED=0317&
    CN= models.CharField(max_length=255) #Testauzore+Testos&
    TRXDATE = models.CharField(max_length=255) #=11/08/10&
    PAYID = models.CharField(max_length=255) #=8628366&
    NCERROR = models.CharField(max_length=255) #=0&
    BRAND = models.CharField(max_length=255) #=VISA&
    IPCTY = models.CharField(max_length=255) #=CH&
    CCCTY = models.CharField(max_length=255) #=US&
    ECI = models.CharField(max_length=255) #=7&
    CVCCheck = models.CharField(max_length=255) #=NO&
    AAVCheck = models.CharField(max_length=255) #=NO&
    VC = models.CharField(max_length=255) #=NO&
    IP = models.CharField(max_length=255) #=84.226.127.220&
    SHASIGN = models.CharField(max_length=255) #=CEE483B0557B8E3437A55094221E15C7DB6A0D63
    
    # Timestamping
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)