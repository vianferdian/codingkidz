from django.contrib import admin
from .models import Project, ProjectSubmission

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'deadline', 'max_score', 'status')
    list_filter = ('status', 'deadline')
    search_fields = ('title', 'course__name')

@admin.register(ProjectSubmission)
class ProjectSubmissionAdmin(admin.ModelAdmin):
    list_display = ('project', 'student', 'status', 'score', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'project__title')
