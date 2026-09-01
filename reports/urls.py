from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('students/', views.student_report, name='student_report'),
    path('students/pdf/', views.student_report_pdf, name='student_report_pdf'),
    path('attendance/', views.attendance_report, name='attendance_report'),
    path('attendance/pdf/', views.attendance_report_pdf, name='attendance_report_pdf'),
    path('payments/', views.payment_report, name='payment_report'),
    path('payments/pdf/', views.payment_report_pdf, name='payment_report_pdf'),
    path('projects/', views.project_report, name='project_report'),
    path('projects/pdf/', views.project_report_pdf, name='project_report_pdf'),
    path('revenue/', views.revenue_report, name='revenue_report'),
    path('revenue/pdf/', views.revenue_report_pdf, name='revenue_report_pdf'),
]
