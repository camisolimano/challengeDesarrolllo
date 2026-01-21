from functools import wraps
from django.http import HttpRequest
from gestionCursos.posthog_client import capture

def track_view_event(event_name: str):
    """
    Decorador que envía un evento a PostHog cada vez que se carga una vista.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request: HttpRequest, *args, **kwargs):
            user = request.user if request.user.is_authenticated else None
            if request.method == "GET":
                capture(
                    user=user,
                    event_name=event_name,
                    properties={
                        "path": request.path,
                        "method": request.method,
                        "client_id": "client_1",
                    }
                )

            return func(request, *args, **kwargs)

        return wrapper
    return decorator
