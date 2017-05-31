from rest.serializers import serializable, optional, Serializer


class AccountSerializer(Serializer):
    def __init__(self, account):
        self.account = account

    @serializable()
    def id(self):
        return self.account.id

    @optional(id)
    def id(self, value):
        self.account.id = value

    @serializable()
    def access_token(self):
        return self.account.access_token

    @optional(access_token)
    def access_token(self, value):
        self.account.access_token = value

    @serializable()
    def username(self):
        return self.account.username

    @optional(username)
    def username(self, value):
        self.account.username = value

    @serializable()
    def full_name(self):
        return self.account.full_name

    @optional(full_name)
    def full_name(self, value):
        self.account.full_name = value

    @serializable()
    def profile_picture(self):
        return self.account.profile_picture

    @optional(profile_picture)
    def profile_picture(self, value):
        self.account.profile_picture = value

    def validate(self):
        self.account.full_clean(exclude=["user"])
        return super().validate()

    def save(self):
        super().save()
        self.account.save()
        return self
