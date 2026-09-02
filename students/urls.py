from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('register/', views.register_student, name='student_register'),
    path('list/', views.student_list, name='student_list'),
    path('add/', views.add_student, name='add_student'),
    path('<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path('<int:student_id>/delete/', views.delete_student, name='delete_student'),
]

