from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('course_session', 'student', 'status', 'check_in_at', 'recorded_by')
    list_filter = ('status', 'created_at')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'course_session__course__name')
