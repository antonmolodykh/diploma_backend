from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^api/account/', include('accounts.urls')),
    url(r'^api/statistics/', include('statistics_profile.urls')),
]
