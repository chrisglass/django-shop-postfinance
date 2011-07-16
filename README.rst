========================
django-shop-postfinance
========================

This application is a postfinance backend for django-SHOP, or any other shop 
system implementing its shop interface.

Usage
======

Add this project to your INSTALLED_APPS, and add 
'shop_postfinance.offsite_postfinance.OffsitePostfinanceBackend' to django-SHOP's 
SHOP_PAYMENT_BACKENDS setting.

Todo
=====

Plenty of stuff is left to do! If you feel like giving a hand, please pick a task
in the follwing list:

* Add a model to store IPN results in the database in full.
* Add a signal on_save() to this model, and only call shop.confirm_payment() 
  from there.
* Port the shop API to other shop systems, so they can also easily use this 
  project as a backend. Examples include but are not limited to: plata, satchmo, 
  lfs
  
Contributing
=============

Feel free to post any comment or suggestion for this project on the django-shop 
mailing list or on #djanho-shop on freenode :)