from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Notification

@login_required(login_url='getskills:login')
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax') == '1':
        return JsonResponse({'status': 'ok'})
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)


@login_required(login_url='getskills:login')
def api_notifications(request):
    unread = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    all_notifs = Notification.objects.filter(user=request.user).order_by('-created_at')[:25]
    
    html = render_to_string('notifications/partial_list.html', {
        'all_notifications': all_notifs,
        'unread_notifications_count': unread.count()
    }, request=request)
    
    return JsonResponse({
        'unread_count': unread.count(),
        'html': html
    })
