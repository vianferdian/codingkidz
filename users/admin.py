from django.contrib import admin
from .models import ActivityLog, CustomUser

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('user__email', 'action', 'description')

if not admin.site.is_registered(CustomUser):
    admin.site.register(CustomUser)
