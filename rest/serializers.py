REGISTERED_FIELDS = {}
REGISTERED_SERIALIZERS = {}


# ------------------------------------------------------------
# Сериализируемое поле
# getter(self)
# ------------------------------------------------------------
def serializable(flag=None, key=None):
    def decorator(getter):
        prop = property(getter)
        REGISTERED_FIELDS[getter] = {
            "name": getter.__name__,
            "serializable": True,
            "editable": False
        }
        if isinstance(flag, str):
            REGISTERED_FIELDS[getter].update({
                "flag": flag,
                "key": flag if key is None else key
            })
        return prop
    return decorator


# ------------------------------------------------------------
# Обязательное поле
# setter(self, value)
# ------------------------------------------------------------
def required(prop):
    if prop.fget not in REGISTERED_FIELDS:
        REGISTERED_FIELDS[prop.fget] = {
            "name": prop.fget.__name__,
            "serializable": False,
        }

    def decorator(setter):
        REGISTERED_FIELDS[prop.fget].update({
            "required": True,
            "editable": True
        })
        return prop.setter(setter)
    return decorator


# ------------------------------------------------------------
# Необязательное поле
# setter(self, value)
# ------------------------------------------------------------
def optional(prop):
    if prop.fget not in REGISTERED_FIELDS:
        REGISTERED_FIELDS[prop.fget] = {
            "name": prop.fget.__name__,
            "serializable": False,
        }

    def decorator(setter):
        REGISTERED_FIELDS[prop.fget].update({
            "required": False,
            "editable": True
        })
        return prop.setter(setter)
    return decorator


# ------------------------------------------------------------
# Базовый класс для работы с изменяемыми моделями
# Для корректной работы нужно:
# 1. Унаследоваться
# 2. Объявить необходимые поля с помощью
#   [serializable, required, optional]
# 3. Переопределить функции update и init(добавить сохранение)
# ------------------------------------------------------------
class Serializer(object):
    @classmethod
    def fields(cls):
        def is_field(field):
            return isinstance(field, property) and field.fget in REGISTERED_FIELDS
        field_array = [
            getattr(cls, attr)
            for attr in dir(cls)
            if is_field(getattr(cls, attr))
        ]
        return [
            REGISTERED_FIELDS[field.fget]
            for field in field_array
        ]

    def serialize(self, *flags):
        result = {}
        for field in self.fields():
            if not field["serializable"]:
                continue

            # Проверяем, что флаг находится в списке флагов
            flag = field.get("flag", None)
            if flag is not None and flag not in flags:
                continue

            name = field["name"]
            key = field.get("key", None)

            # Устанавливаем по ключу
            if key is None or key == "":
                result[name] = getattr(self, field["name"])
            else:
                if key is not None and key not in result:
                    result[key] = {}
                result[key][name] = getattr(self, field["name"])

        return result

    def update(self, **kwargs):
        errors = []
        # Устанавливаем поля и накапливаем ошибки
        for field in self.fields():
            key = field["name"]
            # Отбрасываем поля, которые нельзя редактировать или которые не переданы
            if not field["editable"] or key not in kwargs:
                continue
            try:
                # Устанавливаем значение
                if key in kwargs:
                    setattr(self, key, kwargs[key])
            except Exception as ex:
                errors.append(ex)

        # Выбрасываем полученные ошибки
        if len(errors) > 0:
            raise Exception(*errors)

        # Для цепочечных функций
        return self

    def validate(self):
        return self

    def create(self, **kwargs):
        errors = []
        # Устанавливаем поля и накапливаем ошибки
        for field in self.fields():
            key = field["name"]
            # Отбрасываем поля, которые нельзя редактировать
            if not field["editable"]:
                continue
            try:
                # Отлавливаем обязательные параметры, которые не переданы
                if field["required"] and key not in kwargs:
                    raise Exception("".join("Не передан обязательный параметр " + key))

                # Устанавливаем значение
                if key in kwargs:
                    setattr(self, key, kwargs[key])
            except Exception as ex:
                errors.append(ex)

        # Выбрасываем все полученные ошибки
        if len(errors) > 0:
            raise Exception(*errors)

        # Возвращаем self для цепочек функций:
        # create(**kwargs).validate().save().serialize("details")
        return self

    def save(self):
        return self
