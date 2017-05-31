from accessory_service.response import ResponseHelper
from django.http import JsonResponse
from rest.methods import rest_method
from accessory_service.settings import CLIENT_SECRET
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from accounts.models import Account
from instagram.client import InstagramAPI
from statistics_profile.models import Statistics
import json


def statistics(user):
    api = InstagramAPI(access_token=user.access_token, client_secret=CLIENT_SECRET)
    user = api.user(user.id)

    count_media = user.counts['media']
    follows = user.counts['follows']
    followed_by = user.counts['followed_by']

    # Получаем все медиа
    all_media, next_ = api.user_recent_media(user_id=user.id)
    while next_:
        more_media, next_ = api.user_recent_media(user_id=user.id, with_next_url=next_)
        all_media.extend(more_media)

    likes = 0
    comments = 0
    count_video = 0
    count_images = 0
    last_media = []

    for media in all_media:
        likes += media.like_count
        comments += media.comment_count
        if media.type == "video":
            count_video += 1
        if media.type == "image":
            count_images += 1

    # Среднее вол-во лайков
    likes_average = likes / len(all_media)

    # показатель вовлеченности
    involvement = follows / len(all_media)

    last = Statistics.objects.filter(account=user).last()

    follows_change = last.follows - follows

