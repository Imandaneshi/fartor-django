from django.http import Http404
from rest_framework import exceptions
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import exception_handler

from fartor.globals.api_errors import get_error


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if not isinstance(exc, exceptions.APIException):
        return response

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    error_code = exc.get_codes() if hasattr(exc, 'get_codes') else None
    status_code = exc.status_code or 500
    error = get_error(error_code, return_unknown=False) or {
        "code": error_code,
        "status": status_code,
        "description": exc.detail
    }
    response.data = {
        "ok": False,
        "error": error,
        "status": status_code,
        "data": None
    }
    return response
