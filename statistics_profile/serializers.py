from rest.serializers import serializable, optional, Serializer


class StatisticsSerializer(Serializer):
    def __init__(self, statistics):
        self.statistics = statistics

    @serializable()
    def likes(self):
        return self.statistics.likes

    @serializable()
    def likes_average(self):
        return self.statistics.likes_average

    @serializable()
    def comments(self):
        return self.statistics.comments

    @serializable()
    def follows(self):
        return self.statistics.follows

    @serializable()
    def followed_by(self):
        return self.statistics.followed_by

    @serializable()
    def count_media(self):
        return self.statistics.count_media

    @serializable()
    def count_images(self):
        return self.statistics.count_images

    @serializable()
    def count_videos(self):
        return self.statistics.count_videos

    @serializable()
    def involvement(self):
        return self.statistics.involvement

    @serializable()
    def follows_change(self):
        return self.statistics.follows_change
