from django.conf.urls import url
from statistics_profile.api import test

urlpatterns = [
    url(r'^test/$', test),
]