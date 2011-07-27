#-*- coding: utf-8 -*-

from django.contrib import admin
from shop_postfinance.models import PostfinanceIPN

admin.site.register(PostfinanceIPN) # This will be a little ugly... but necessary