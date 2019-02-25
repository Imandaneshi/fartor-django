import graphene

from fartor.globals.api_errors import get_error
from fartor.modules.graphql.objects.error import GraphqlError


class GraphqlBaseQuery(graphene.ObjectType):
    ok = graphene.Boolean()
    error = graphene.Field(GraphqlError, required=False)

    @staticmethod
    def resolve_ok(res, *args, **kwargs):
        return res.get('ok', False)

    @staticmethod
    def resolve_error(res, *args, **kwargs):
        return res.get('error', None)

    @staticmethod
    def success_response(**kwargs):
        """
        This function returns a successful response

        :return: successful Response
        """

        return dict(ok=True, error=None, **kwargs)

    @staticmethod
    def error_response(error_code, details=None, **kwargs):
        """
        This function returns an error response

        :param error_code: error code specified in api_errors
        :param details: error details if any
        :type error_code: str,
        :type details: dict, list, int, str, boolean, float
        :return: error Response
        """

        error = get_error(error_code, return_unknown=True, details=details)
        return dict(ok=False, error=error, **kwargs)


class GraphqlBaseMutation(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.Field(GraphqlError, required=False)

    @staticmethod
    def mutate(*args, **kwargs):
        raise NotImplemented

    @staticmethod
    def success_response(mutation, **kwargs):
        """
        This function returns a successful response

        :param mutation: graphql mutation
        :return: successful Response
        """

        return mutation(ok=True, error=None, **kwargs)

    @staticmethod
    def error_response(mutation, error_code, details=None, **kwargs):
        """
        This function returns an error response

        :param error_code: error code specified in api_errors
        :param mutation: graphql mutation
        :param details: error details if any
        :type error_code: str,
        :type details: dict, list, int, str, boolean, float
        :return: error Response
        """

        error = get_error(error_code, return_unknown=True, details=details)
        return mutation(ok=False, error=error, **kwargs)
