from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('list/', views.attendance_list, name='attendance_list'),
    path('add/', views.add_attendance, name='add_attendance'),
    path('<int:attendance_id>/edit/', views.edit_attendance, name='edit_attendance'),
    path('tutor-take/<int:session_id>/', views.tutor_take_attendance, name='tutor_take_attendance'),
    path('tutor-submit-ajax/', views.tutor_submit_attendance_ajax, name='tutor_submit_attendance_ajax'),
]
