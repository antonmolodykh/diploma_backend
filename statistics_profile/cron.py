import datetime

from accounts.models import Profile
from statistics_profile.statistic import statistics


def scheduler():
    hour = datetime.datetime.now().hour
    all_profiles = Profile.objects.all()
    for profile in all_profiles:
        if profile.hour == hour:
            statistics(profile)
