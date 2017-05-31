from accessory_service.response import ResponseHelper
from django.http import JsonResponse
from rest.methods import rest_method
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from accounts.models import Account
import requests
import json


@rest_method("POST")
def account_register(request, email, password, access_token):
    # Пользователь должен выйти из системы перед регистрацией
    print ("test")
    if Account.from_request(request) is not None:
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

    # Регистрируем пользователя
    user = User.objects.create_user(email=email, username=email, password=password)

    # Создаем профиль пользователя
    account = Account(
        id=id,
        access_token=access_token,
        username=username,
        full_name=full_name,
        user=user,
        profile_picture=profile_picture
    ).serializer.create().validate().save()

    auth.login(request, user)

    # Возвращаем созданный профиль
    return JsonResponse(account.serialize())


@rest_method("POST", "GET")
def account_login(request, email, password):
    account = Account.from_request(request)
    if account is not None:
        return JsonResponse(account.serializer.serialize())

    user = auth.authenticate(username=email, password=password)

    if user is None:
        raise Exception("Неверный логин или пароль")

    auth.login(request, user)

    account = Account.objects.filter(user=user).first()
    return JsonResponse(account.serializer.serialize())


@rest_method("POST")
def account_logout(request):
    auth.logout(request)
    return ResponseHelper.success()
