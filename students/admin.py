from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_code', 'user', 'school_name', 'parent_name', 'status')
    list_filter = ('status', 'gender')
    search_fields = ('student_code', 'user__first_name', 'user__last_name', 'school_name')

