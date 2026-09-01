from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
    path('api-notifications/', views.api_notifications, name='api_notifications'),
]
