from django.contrib import auth
from django.db import models
from django.contrib.auth.models import User
from accounts.serializers import ProfileSerializer


class Profile(models.Model):
    class Meta:
        db_table = 'profile'

    # Владелец профиля
    user = models.OneToOneField(User, related_name="profile")

    # Id from Instagram
    id = models.IntegerField(primary_key=True)

    # Access_token from Instagram
    access_token = models.TextField(max_length=50)

    # Username from Instagram
    username = models.CharField(max_length=50)

    # Full name from Instagram
    full_name = models.CharField(max_length=50, blank=True)

    # Avatar from Instagram
    profile_picture = models.TextField(blank=True)

    hour = models.IntegerField(null=True)

    # Сериализатор
    @property
    def serializer(self):
        return ProfileSerializer(self)

    # Получить профиль пользователя из пользователя
    @staticmethod
    def from_user(user):
        if hasattr(user, "profile"):
            return user.profile
        return None

    # Получить профиль пользователя из запроса
    @staticmethod
    def from_request(request):
        return Profile.from_user(auth.get_user(request))
