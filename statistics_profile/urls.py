from django.conf.urls import url
from statistics_profile.api import test, test2, test3

urlpatterns = [
    url(r'^test/$', test),
    url(r'^test2/$', test2),
    url(r'^test3/$', test3),
]