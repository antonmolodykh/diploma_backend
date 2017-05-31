from django.db import models
from accounts.models import Profile
from statistics_profile.serializers import StatisticsSerializer


class Statistics(models.Model):
    class Meta:
        db_table = 'statistics'

    profile = models.ForeignKey(Profile, related_name='+', null=True)

    likes = models.IntegerField(default=0)

    likes_average = models.DecimalField(max_digits=8, decimal_places=2, default=0) #

    comments = models.IntegerField(default=0)

    follows = models.IntegerField(default=0)

    followed_by = models.IntegerField(default=0)
    # Общее количество публикаций
    count_media = models.IntegerField(default=0)

    count_images = models.IntegerField(default=0)

    count_videos = models.IntegerField(default=0)
    # Показатель вовлеченности
    involvement = models.DecimalField(max_digits=6, decimal_places=4, default=0)

    follows_change = models.IntegerField(default=0)

    @property
    def serializer(self):
        return StatisticsSerializer(self)
