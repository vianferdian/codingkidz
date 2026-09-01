from dz import dz_array
from notifications.models import Notification

'''
A context processor is a function that accepts an argument and returns a dictionary as its output.
In our case, the returning dictionary is added as the context and the biggest advantage is that,
it can be accessed globally i.e, across all templates. 
'''

def dz_static(request):
    # we can send data as {"dz_array":dz_array} than you get all dict, using <h1>{{ dz_array }}</h1>
    return {"dz_array":dz_array}


def notifications_context(request):
    if request.user and request.user.is_authenticated:
        unread = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
        all_notifs = Notification.objects.filter(user=request.user).order_by('-created_at')[:25]
        return {
            'unread_notifications': unread,
            'unread_notifications_count': unread.count(),
            'all_notifications': all_notifs
        }
    return {}

