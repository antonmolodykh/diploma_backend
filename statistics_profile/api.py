from accessory_service.response import ResponseHelper
from django.http import JsonResponse
from rest.methods import rest_method
from accessory_service.settings import CLIENT_SECRET
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from accounts.models import Profile
from instagram.client import InstagramAPI
from statistics_profile.models import Statistics
import datetime
import json

@rest_method("GET")
def test(request):
    # Аутентификация
    profile = Profile.from_request(request)
    print('one')
    if profile is None:
        raise Exception("Залогиньтесь, сударь!")
    api = InstagramAPI(access_token=profile.access_token, client_secret=CLIENT_SECRET)

    # Инфа по юзеру
    account = api.user(profile.id)
    count_media = account.counts['media']
    follows = account.counts['follows']
    followed_by = account.counts['followed_by']

    # Сортировки
    def sort_by_like(target):
        return target.like_count

    def sort_by_comments(target):
        return target.comment_count

    # Получаем все медиа
    all_media, next_ = api.user_recent_media(user_id=profile.id)
    while next_:
        more_media, next_ = api.user_recent_media(user_id=profile.id, with_next_url=next_)
        all_media.extend(more_media)

    # Инициализация основных параментров
    likes = 0
    comments = 0
    count_video = 0
    count_photo = 0
    prepare_hours = [[0, 0] for i in range(24)]
    tags = []
    filters = []
    last_media = []

    # обработка всех медиа
    for media in all_media:
        likes += media.like_count
        comments += media.comment_count
        if media.type == "video":
            count_video += 1
        if media.type == "image":
            count_photo += 1

        # распределение по времени
        prepare_hours[media.created_time.hour][0] += 1
        prepare_hours[media.created_time.hour][1] += media.like_count


    # распределение по времени в преглядном виде
    hours = [b/a if a is not 0 else 0 for a, b in prepare_hours]

    # получаем вчерашний день
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

    # последние медиа (за последний день)
    for media in all_media:
        if media.created_time < yesterday:
            break
        target = {
            'image': media.images['thumbnail'].url,
            'like_count': media.like_count,
            'comment_count': media.comment_count
        }
        last_media.append(target)



    # самые обсуждаемые медиа
    all_media.sort(key=sort_by_comments, reverse=True)
    max_comments = all_media[:3]
    max_comments_images = []
    for media in max_comments:
        max_comments_images.append(media.images['thumbnail'].url)

    # самые популярные медиа
    all_media.sort(key=sort_by_like, reverse=True)
    max_like = all_media[:3]

    max_like_images = []
    for media in max_like:
        max_like_images.append(media.images['thumbnail'].url)
        tags.extend([tag.name for tag in media.tags])
        filters.append(media.filter)


    # Среднее вол-во лайков
    likes_average = likes/len(all_media)

    # показатель вовлеченности
    involvement = follows/len(all_media)

    # формирование отета
    response = {}

    profile = {
        'username': account.username,
        'full_name': account.full_name,
        'profile_picture': account.profile_picture,
    }
    report = {
        'follows': follows,
        'followed_by': followed_by,
        'count_media': count_media,
        'count_video': count_video,
        'count_photo': count_photo,
        'likes': likes,
        'comments': comments,
        'tags': tags,
        'max_like': max_like_images,
        'max_comments': max_comments_images,
        'filters': filters,
        'likes_average': likes_average,
        'involvement': involvement,
        'hours': hours,
        'last_media': last_media
    }
    response["profile"] = profile
    response["report"] = report

    return JsonResponse(response)