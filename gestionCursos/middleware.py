import traceback
import sys
from django.utils.deprecation import MiddlewareMixin
from gestionCursos.posthog_client import posthog_client

class PostHogExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        traceback_str = ''.join(tb_lines)
        
        error_properties = {
            '$exception_type': exc_type.__name__ if exc_type else 'Unknown',
            '$exception_message': str(exception),
            '$exception_traceback': traceback_str,
            'path': request.path,
            'method': request.method,
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'url': request.build_absolute_uri(),
        }
        
        if request.GET:
            error_properties['query_params'] = dict(request.GET)
        
        if getattr(request, "user", None) and request.user.is_authenticated:
            distinct_id = str(request.user.id)
        else:
            distinct_id = "anonymous"
        posthog_client.capture_exception(
            exception,
            distinct_id=distinct_id,
            properties=error_properties,
        )
        
        return None
    
    
class PostHogCSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Content-Security-Policy"] = (
            "frame-ancestors 'self' https://us.posthog.com"
        )
        return response