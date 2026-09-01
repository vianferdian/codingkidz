from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.project_list, name='project_list'),
    path('submissions/', views.submission_list, name='submission_list'),
    path('add/', views.add_project, name='add_project'),
    path('<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('<int:project_id>/submit/', views.submit_project, name='submit_project'),
    path('submissions/<int:submission_id>/review/', views.review_submission, name='review_submission'),
]
