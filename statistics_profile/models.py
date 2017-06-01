from django.db import models
from accounts.models import Profile
from statistics_profile.serializers import StatisticsSerializer


class Statistics(models.Model):
    class Meta:
        db_table = 'statistics'

    profile = models.ForeignKey(Profile, related_name='+', null=True)

    likes = models.IntegerField(null=True)

    likes_average = models.DecimalField(max_digits=8, decimal_places=2, null=True) #

    comments = models.IntegerField(null=True)

    follows = models.IntegerField(null=True)

    followed_by = models.IntegerField(null=True)
    # Общее количество публикаций
    count_media = models.IntegerField(null=True)

    count_images = models.IntegerField(null=True)

    count_videos = models.IntegerField(null=True)
    # Показатель вовлеченности
    involvement = models.DecimalField(max_digits=6, decimal_places=4, null=True)

    @property
    def serializer(self):
        return StatisticsSerializer(self)
