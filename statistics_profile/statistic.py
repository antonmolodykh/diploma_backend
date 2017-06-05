from accessory_service.response import ResponseHelper
from django.http import JsonResponse
from rest.methods import rest_method
from accessory_service.settings import CLIENT_SECRET
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from accounts.models import Profile
from instagram.client import InstagramAPI
from statistics_profile.models import Statistics
import json


def statistics(profile):
    profile = profile
    api = InstagramAPI(access_token=profile.access_token, client_secret=CLIENT_SECRET)

    account = api.user(profile.id)

    count_media = account.counts['media']
    follows = account.counts['follows']
    followed_by = account.counts['followed_by']

    # Получаем все медиа
    all_media, next_ = api.user_recent_media(user_id=profile.id)
    while next_:
        more_media, next_ = api.user_recent_media(user_id=profile.id, with_next_url=next_)
        all_media.extend(more_media)

    likes = 0
    comments = 0
    count_videos = 0
    count_images = 0

    for media in all_media:
        likes += media.like_count
        comments += media.comment_count
        if media.type == "video":
            count_videos += 1
        if media.type == "image":
            count_images += 1

    # Среднее вол-во лайков
    likes_average = likes / len(all_media)

    # показатель вовлеченности
    involvement = (likes_average/follows)*100

    statistics = Statistics(
        profile=profile,
        likes=likes,
        likes_average=likes_average,
        comments=comments,
        follows=follows,
        followed_by=followed_by,
        count_media=count_media,
        count_images=count_images,
        count_videos=count_videos,
        involvement=involvement
    )
    statistics.save()
