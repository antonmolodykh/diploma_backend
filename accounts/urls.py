from django.conf.urls import url
from accounts.api import account_register, account_login, account_logout

urlpatterns = [
    url(r'^register/$', account_register),
    url(r'^login/$', account_login),
    url(r'^logout/$', account_logout),
]