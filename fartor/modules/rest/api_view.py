from django.conf import settings
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import status as status_codes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from fartor.globals.api_errors import get_error
from fartor.modules.rest.auth import CsrfExemptSessionAuthentication

# Only allow OAuth2 authentication when debug is False otherwise
#  allow SessionAuthentication and TokenAuthentication for debugging purposes
authentication_classes = (OAuth2Authentication,
                          CsrfExemptSessionAuthentication,
                          TokenAuthentication) if settings.DEBUG else (OAuth2Authentication,)


class CustomAPIView(APIView):
    authentication_classes = authentication_classes

    def validate_post_body(self):
        """
        This function validates the post body by the serializer specified in views serializer_class attribute

        :return: a directory of validated items
        """
        if hasattr(self, 'serializer_class'):
            data = self.request.data
            ser = self.serializer_class(data=data)
            try:
                ser.is_valid(raise_exception=True)
            except Exception as e:
                return None, e.detail if hasattr(e, 'detail') else None
            return ser.validated_data, None

        return None, None

    def validate_get_params(self):
        """
        This function validates the query params by the serializer specified in views params_serializer_class attribute

        :return: a directory of validated items
        """

        if hasattr(self, 'params_serializer_class'):
            data = self.request.query_params
            ser = self.params_serializer_class(data=data)
            try:
                ser.is_valid(raise_exception=True)
            except Exception as e:
                return None, e.detail if hasattr(e, 'detail') else None
            return ser.validated_data, None
        return None, None

    def make_success_response(self, data=None, status_code=status_codes.HTTP_200_OK):
        """
        This function returns a successful response

        :param data: data if there is any, an empty response would return if this param is None
        :param status_code: response status code
        :type data: dict, list, int, str, boolean, float
        :type status_code: int
        :return: successful Response
        """

        return Response({
            "ok": True,
            "error": None,
            "status": status_code,
            "data": data or None
        }, status=status_code)

    def make_error_response(self, error_code, details=None):
        """
        This function returns an error response

        :param error_code: error code specified in api_errors
        :param details: error details if any
        :type error_code: str,
        :type details: dict, list, int, str, boolean, float
        :return: error Response
        """

        error = get_error(error_code, return_unknown=True, details=details)
        return Response({
            "ok": True,
            "error": error,
            "status": error['status'],
            "data": None,
        }, status=error['status'])
