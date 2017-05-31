from django.contrib import auth
from django.db import models
from django.contrib.auth.models import User
from accounts.serializers import AccountSerializer


class Account(models.Model):
    class Meta:
        db_table = 'accounts'

    # Владелец профиля
    user = models.OneToOneField(User, related_name="account")

    # Id from Instagram
    id = models.IntegerField(primary_key=True)

    # Access_token from Instagram
    access_token = models.TextField(max_length=50)

    # Username from Instagram
    username = models.CharField(max_length=50)

    # Full name from Instagram
    full_name = models.CharField(max_length=50, blank=True)

    # Avatar from Instagram
    profile_picture = models.CharField(max_length=100, blank=True)

    # Сериализатор
    @property
    def serializer(self):
        return AccountSerializer(self)

    # Получить профиль пользователя из пользователя
    @staticmethod
    def from_user(user):
        if hasattr(user, "account"):
            return user.account
        return None

    # Получить профиль пользователя из запроса
    @staticmethod
    def from_request(request):
        return Account.from_user(auth.get_user(request))