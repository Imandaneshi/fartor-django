from django.utils.deprecation import MiddlewareMixin


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    return ip


class IpMiddleware(MiddlewareMixin):
    """
    This middleware attaches the ip to request object

    .. todo:: check for blocked ip addresses
    """

    def process_request(self, request):
        # attach the ip address to request
        request.ip = get_client_ip(request)
