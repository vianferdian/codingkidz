from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

def create_notification(user, title, message, notification_type='SYSTEM'):
    """
    Utility function to create a new notification for a user.
    """
    if user:
        return Notification.objects.create(
            user=user,
            title=title,
            message=message,
            type=notification_type
        )
    return None
