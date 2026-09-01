from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    path('courses/', views.course_list, name='course_list'),
    path('course/', views.course_list),  # Alias singular
    path('courses/add/', views.add_course, name='add_course'),
    path('course/add/', views.add_course),
    path('courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('course/<int:course_id>/edit/', views.edit_course),
    path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('course/<int:course_id>/delete/', views.delete_course),
    path('classes/', views.class_list, name='class_list'),
    path('class/', views.class_list),
    path('classes/add/', views.add_enrollment, name='add_enrollment'),
    path('classes/<int:enrollment_id>/edit/', views.edit_enrollment, name='edit_enrollment'),
    path('classes/<int:enrollment_id>/delete/', views.delete_enrollment, name='delete_enrollment'),
    path('sessions/', views.session_list, name='session_list'),
    path('session/', views.session_list),
    path('sessions/add/', views.add_session, name='add_session'),
    path('sessions/<int:session_id>/edit/', views.edit_session, name='edit_session'),
    path('sessions/<int:session_id>/delete/', views.delete_session, name='delete_session'),
]
