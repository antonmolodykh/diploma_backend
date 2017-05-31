from django.db import models
from accounts.models import Account
from statistics_profile.serializers import StatisticsSerializer


class Statistics(models.Model):
    class Meta:
        db_table = 'statistics'

    # account = models.ForeignKey(Account, related_name='+')
    #
    # likes = models.IntegerField()
    #
    # likes_average = models.DecimalField(max_digits=8, decimal_places=2)
    #
    # comments = models.IntegerField()
    #
    # follows = models.IntegerField()
    #
    # followed_by = models.IntegerField()
    # # Общее количество публикаций
    # count_media = models.IntegerField()
    #
    # count_images = models.IntegerField()
    #
    # count_videos = models.IntegerField()
    # # Показатель вовлеченности
    # Involvement = models.DecimalField(max_digits=6, decimal_places=4, default=0)

    @property
    def serializer(self):
        return StatisticsSerializer(self)
