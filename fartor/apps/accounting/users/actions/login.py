import graphene
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from rest_framework import serializers

from fartor.apps.accounting.users.models import LoginHistory
from fartor.apps.accounting.users.object_types import UserSelf
from fartor.apps.accounting.users.serializers import UserSelfSerializers
from fartor.modules.graphql.base_object import GraphqlBaseMutation
# Graphql
from fartor.modules.rest.api_view import CustomAPIView


def login(username, password, request):
    """
    this function authenticates the user

    :param username: input username
    :type username: str
    :param password: input password
    :type password: str
    :param request: request object
    :return: User, error_code
    """

    # check whatever user exist and is active
    validate_user = get_user_model().objects.filter(username=username, is_active=True).first()
    if validate_user is None:
        return None, 'user_not_found'
    # check if the input password is correct
    user = authenticate(request, username=username, password=password)
    if user:
        # authenticate user
        auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        # create a successful login history for `user`
        LoginHistory.create_history(user, ip=request.ip, successful=True)
        # return a user object
        return user, None
    else:
        # create a failed login history for user
        LoginHistory.create_history(user, ip=request.ip, successful=False)
        # return a `wrong_password` error
        return None, 'wrong_password'


class LoginMutation(GraphqlBaseMutation):
    class Arguments:
        username = graphene.String()
        password = graphene.String()

    self = graphene.Field(lambda: UserSelf)

    @staticmethod
    def mutate(root, info, username, password):
        request = info.context
        # try to authenticate user
        user, error = login(username=username, password=password, request=request)
        return LoginMutation.success_response(LoginMutation, user=user) \
            if user else LoginMutation.error_response(LoginMutation, error_code=error, user=None)


# Rest API

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, max_length=300, required=True)

    def update(self, instance, validated_data):
        raise NotImplemented

    def create(self, validated_data):
        raise NotImplemented


class LoginRestAPI(CustomAPIView):
    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        data, details = self.validate_post_body()
        if data is None:
            return self.make_error_response('validation_error', details=details)
        else:
            user, error = login(username=data['username'],
                                password=data['password'],
                                request=request)
            data = UserSelfSerializers(user).data if user else None
            return self.make_success_response(data) \
                if user else self.make_error_response(error)
