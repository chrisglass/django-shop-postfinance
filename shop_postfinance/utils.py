#-*- coding: utf-8 -*-

from django.conf import settings
import hashlib

def security_check(data, secret_key):
    '''
    Performs a postfinance security check. That is, it compares the SHA1 provided by the request to
    a SHA1 sum of the parameters (passed via GET or POST), ordered alphabetically, and separated by the
    secret key.

    Data should be a dictionnary, as provided by a request's POST or GET
    '''
    cap_data = {}
    string_list = []
    secret_key = settings.POSTFINANCE_SECRET_KEY

    for key, val in data.iteritems():
        cap_data[key.upper()] = val # make all keys capital letters

    for key in sorted(cap_data.keys()):
        if key != 'SHASIGN':
#            if key == 'AMOUNT': # Must be: cap_data['AMOUNT'] = "%.0f" % (cap_data['AMOUNT']*100)
#                entry = "%s=%.0f" % (key,float(cap_data[key])*100)
#            else:
            entry = "%s=%s" % (key,cap_data[key])
            string_list.append(entry)

    # Now we have a sorted list of parameters that have capital keys (like the doc says)

    hash_string = secret_key.join(string_list)
    hash_string = "%s%s" % (hash_string,secret_key)

    #hash_string =  "AMOUNT=%s%sCURRENCY=%s%sLANGUAGE=%s%sORDERID=%s%sPSPID=%s%s" #% (amount, key, currency, key, language, key, order_id, key, pspid, key)
    s = hashlib.sha1()
    s.update(hash_string)
    hex = s.hexdigest().upper()
    original =  data['SHASIGN']
    return hex == original


def compute_security_checksum(**data):
    ''' Used to send a security checksum of parameters to postfinance '''
    secret_key = settings.POSTFINANCE_SECRET_KEY
    contents = dict([(key.upper(), value) for key, value in data.items()])
    hash_string = ""
    for key, value in sorted(contents.items()):
        hash_string += "%s=%s%s" % (key, value, secret_key)
    output = hashlib.sha1(hash_string).hexdigest().upper()
    return output
