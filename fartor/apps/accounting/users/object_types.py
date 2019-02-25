import graphene


class UserBase(object):
    id = graphene.ID()
    username = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()

    @staticmethod
    def resolve_id(user, *args, **kwargs):
        return user.public_id

    @staticmethod
    def resolve_username(user, *args, **kwargs):
        return user.username

    @staticmethod
    def resolve_first_name(user, *args, **kwargs):
        return user.first_name

    @staticmethod
    def resolve_last_name(user, *args, **kwargs):
        return user.last_name


class UserSelf(UserBase, graphene.ObjectType):
    date_joined = graphene.DateTime()

    @staticmethod
    def resolve_last_name(user, *args, **kwargs):
        return user.date_joined
