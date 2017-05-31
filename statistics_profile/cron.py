from statistics_profile.models import Statistics


def scheduler():
    statistic = Statistics(
        likes=22
    )
    statistic.save()

