from django.http import JsonResponse


class JsonResponseHelper:
    @staticmethod
    def success(**kwargs):
        json = {'status': 'success'}
        json.update(kwargs)
        return JsonResponse(json)

    @staticmethod
    def error(description, **kwargs):
        json = {'status': 'error', 'description': description}
        json.update(kwargs)
        return JsonResponse(json)


class ResponseHelper:
    @staticmethod
    def failed_json(error_list, **kwargs):
        json = {'errors': error_list}
        json.update(kwargs)
        return json

    @staticmethod
    def failed(error_list, **kwargs):
        return JsonResponse(ResponseHelper.failed_json(error_list, **kwargs))

    @staticmethod
    def success(**kwargs):
        return JsonResponse(kwargs)


class ResponseError(JsonResponse):
    def __init__(self, *errors):
        super().__init__({"errors": errors})
