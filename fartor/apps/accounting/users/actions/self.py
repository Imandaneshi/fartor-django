import graphene

from fartor.apps.accounting.users.object_types import UserSelf
from fartor.apps.accounting.users.serializers import UserSelfSerializers
from fartor.modules.graphql.base_object import GraphqlBaseQuery
# Graphql
from fartor.modules.rest.api_view import CustomAPIView


def get_self(request):
    """
    this function returns request's user if any

    :param request: request object
    :return: User, error_code
    """
    return (request.user, None) if \
        request.user.is_authenticated else (None, 'not_authenticated')


class SelfQuery(GraphqlBaseQuery):
    self = graphene.Field(lambda: UserSelf)

    @staticmethod
    def resolve_self(root, info):
        return root['self']


class GetSelfQuery:
    get_self = graphene.Field(SelfQuery)

    @staticmethod
    def resolve_get_self(root, info, *args, **kwargs):
        request = info.context
        # try to get user's object
        self, error = get_self(request)
        return GraphqlBaseQuery.success_response(self=self) \
            if self else GraphqlBaseQuery.error_response(error_code=error, self=None)


class SelfRestAPI(CustomAPIView):

    def get(self, request, *args, **kwargs):
        user, error = get_self(request=request)
        data = UserSelfSerializers(user).data if user else None
        return self.make_success_response(data) \
            if user else self.make_error_response(error)
