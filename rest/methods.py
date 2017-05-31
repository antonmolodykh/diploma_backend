from inspect import signature
from django.http.response import JsonResponse



def rest_method(*methods):
    def decorator(func):
        # Получаем информацию о параметрах функции
        has_args = False
        has_kwargs = False
        parameter_list = []
        required_list = []
        has_request = False
        for parameter in signature(func).parameters.values():
            if parameter.kind not in [parameter.VAR_POSITIONAL, parameter.VAR_KEYWORD]:
                if parameter.name == "request":
                    has_request = True
                elif parameter.default == parameter.empty:
                    required_list.append(parameter.name)
                parameter_list.append(parameter.name)
            else:
                has_args = has_args or parameter.kind == parameter.VAR_POSITIONAL
                has_kwargs = has_kwargs or parameter.kind == parameter.VAR_KEYWORD

        # Обрабатываем запрос
        def wrapper(request):
            try:
                if request.method not in methods:
                    raise Exception("Неразрешенный метод")

                params = dict(getattr(request, request.method).items())
                params.update(dict(request.FILES))

                missing = set(required_list) - set(params)
                if len(missing) > 0:
                    raise Exception("Отсутствуют обязательные аргументы: " + str(list(missing)))

                args = [request] if has_request or has_args else []
                kwargs = params if has_kwargs else {
                    key: params[key]
                    for key in params
                    if key in parameter_list
                }

                return func(*args, **kwargs)
            except Exception as ex:
                return JsonResponse({
                    "errors": (ex.args)
                })

        return wrapper
    return decorator
