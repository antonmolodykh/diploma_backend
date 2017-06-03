from django.http import JsonResponse
from rest.methods import rest_method
from accessory_service.settings import CLIENT_SECRET
from accounts.models import Profile
from instagram.client import InstagramAPI
from statistics_profile.models import Statistics
import datetime
from statistics_profile.statistic import statistics


@rest_method("GET")
def get_report(request):
    # Аутентификация
    profile = Profile.from_request(request)
    if profile is None:
        raise Exception("Залогиньтесь, сударь!")
    api = InstagramAPI(access_token=profile.access_token, client_secret=CLIENT_SECRET)

    # Инфа по юзеру
    account = api.user(profile.id)
    count_media = account.counts['media']
    follows = account.counts['follows']
    followed_by = account.counts['followed_by']

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
    filters_dict = {}
    filters_list = []
    tags_dict = {}
    tags_list = []
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

        # фильтры
        if filters_dict.get(media.filter):
            filters_dict[media.filter][0] += 1
            filters_dict[media.filter][1] += media.like_count
        else:
            filters_dict[media.filter] = [1, media.like_count]

        # хэштеги
        for tag in media.tags:
            if tags_dict.get(tag.name):
                tags_dict[tag.name][0] += 1
                tags_dict[tag.name][1] += media.like_count
            else:
                tags_dict[tag.name] = [1, media.like_count]

    # формирование списка фильтров
    for key, value in filters_dict.items():
        filters_list.append((key, value[1]/value[0]))
    filters_list.sort(key=lambda x: x[1], reverse=True)

    if len(filters_list) > 3:
        filters = [a for a, b in filters_list[:3]]
    else:
        filters = [a for a, b in filters_list]

    # формирование списка тегов
    for key, value in tags_dict.items():
        tags_list.append((key, value[1] / value[0]))
        tags_list.sort(key=lambda x: x[1], reverse=True)

    if len(tags_list) > 10:
        tags = [a for a, b in tags_list[:10]]
    else:
        tags = [a for a, b in tags_list]

    # распределение по времени в преглядном виде
    hours = [b/a if a is not 0 else 0 for a, b in prepare_hours]

    # получаем вчерашний день
    yesterday = datetime.datetime.now() - datetime.timedelta(days=7)

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
    all_media.sort(key=lambda x: x.comment_count, reverse=True)
    max_comments = all_media[:3]
    max_comments_images = []
    for media in max_comments:
        max_comments_images.append({
            'image': media.images['thumbnail'].url,
            'like_count': media.like_count,
            'comment_count': media.comment_count
        })

    # самые популярные медиа
    all_media.sort(key=lambda x: x.like_count, reverse=True)
    max_like = all_media[:3]

    max_like_images = []
    for media in max_like:
        max_like_images.append({
            'image': media.images['thumbnail'].url,
            'like_count': media.like_count,
            'comment_count': media.comment_count
        })


    # Среднее вол-во лайков
    likes_average = likes/len(all_media)

    # показатель вовлеченности
    involvement = (likes_average/follows)*100

    # формирование отета
    response = {
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
        'involvement': round(involvement, 1),
        'hours': hours,
        'last_media': last_media
    }

    return JsonResponse(response)


@rest_method("GET")
def test2(request):
    profile = Profile.from_request(request)
    print('one')
    if profile is None:
        raise Exception("Залогиньтесь, сударь!")

    return statistics(profile)


@rest_method("POST")
def get_statistics(request, count=7):
    profile = Profile.from_request(request)
    print('one')
    if profile is None:
        raise Exception("Залогиньтесь, сударь!")

    all_statistics = Statistics.objects.all()
    if len(all_statistics) < int(count):
        necessary_statistics = all_statistics
    else:
        necessary_statistics = all_statistics[:int(count)]

    response = {
        'likes': [],
        'likes_average': [],
        'comments': [],
        'follows': [],
        'followed_by': [],
        'count_media': [],
        'count_images': [],
        'count_videos': [],
        'involvement': [],
    }

    for statistics in necessary_statistics:
        response['likes'].append(statistics.likes)
        response['likes_average'].append(statistics.likes_average)
        response['comments'].append(statistics.comments)
        response['follows'].append(statistics.follows)
        response['followed_by'].append(statistics.followed_by)
        response['count_media'].append(statistics.count_media)
        response['count_images'].append(statistics.count_images)
        response['count_videos'].append(statistics.count_videos)
        response['involvement'].append(statistics.involvement)



    return JsonResponse(response)