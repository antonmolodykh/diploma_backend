from django.conf.urls import url
from statistics_profile.api import test2, get_statistics, get_report

urlpatterns = [
    url(r'^report/$', get_report),
    url(r'^test2/$', test2),
    url(r'^statistics/$', get_statistics),
]