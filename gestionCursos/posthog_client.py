from posthog import Posthog
from django.conf import settings

posthog_client = Posthog(
    project_api_key=settings.POSTHOG_API_KEY,
    host=settings.POSTHOG_HOST,
    enable_exception_autocapture= False
)

def capture(user, event_name: str, properties: dict | None = None) -> None:
    if user is not None and getattr(user, "is_authenticated", False):
        distinct_id = str(user.id)
    else:
        distinct_id = "anonymous"
    
    props = dict(properties or {})

    props.setdefault("client_id", "client_2")

    posthog_client.capture(
        distinct_id=distinct_id,
        event=event_name,
        properties=props,
    )