import random

from accessory_service.response import ResponseHelper
from django.http import JsonResponse
from rest.methods import rest_method
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from accounts.models import Profile
import requests
import json


@rest_method("POST")
def account_register(request, email, password, access_token):
    # Пользователь должен выйти из системы перед регистрацией
    if Profile.from_request(request) is not None:
        raise Exception("Вы уже зарегистрированы")

    if User.objects.filter(email=email).first() is not None:
        raise Exception("Пользователь с таким e-mail уже зарегестрирован")

    params = {'access_token': access_token}
    req = requests.get("https://api.instagram.com/v1/users/self",params=params)
    resp = json.loads((req.content).decode('utf-8'))
    user_data = resp['data']

    id = user_data['id']
    username = user_data['username']
    full_name = user_data['full_name']
    profile_picture = user_data['profile_picture']

    hour = random.randint(0,23)
    # Регистрируем пользователя
    user = User.objects.create_user(email=email, username=email, password=password)

    # Создаем профиль пользователя
    profile = Profile(
        id=id,
        access_token=access_token,
        username=username,
        full_name=full_name,
        user=user,
        profile_picture=profile_picture,
        hour=hour
    ).save()

    auth.login(request, user)

    # Возвращаем созданный профиль
    return ResponseHelper.success()


@rest_method("POST", "GET")
def account_login(request, email, password):
    account = Profile.from_request(request)
    if account is not None:
        raise Exception("Прежде разлогиньтесь, сударь!")

    user = auth.authenticate(username=email, password=password)

    if user is None:
        raise Exception("Неверный логин или пароль")

    auth.login(request, user)

    profile = Profile.objects.filter(user=user).first()
    return JsonResponse({
        'id': profile.id,
        'access_token': profile.access_token,
        'username': profile.username,
        'full_name': profile.full_name,
        'profile_picture': profile.profile_picture,
        'hour': profile.hour
    })


@rest_method("GET")
def account_logout(request):
    auth.logout(request)
    return ResponseHelper.success()


@rest_method("GET")
def account_my(request):
    profile = Profile.from_request(request)
    if profile is None:
        raise Exception("Прежде залогиньтесь, сударь!")

    return JsonResponse({
        'id': profile.id,
        'access_token': profile.access_token,
        'username': profile.username,
        'full_name': profile.full_name,
        'profile_picture': profile.profile_picture,
        'hour': profile.hour
    })