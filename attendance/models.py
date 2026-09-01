from django.db import models
from django.conf import settings
from academics.models import CourseSession
from students.models import Student

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('HADIR', 'Hadir'),
        ('IZIN', 'Izin'),
        ('SAKIT', 'Sakit'),
        ('ALPA', 'Alpa'),
    )
    course_session = models.ForeignKey(CourseSession, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    check_in_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('course_session', 'student')

    def __str__(self):
        return f"{self.student} -> Session #{self.course_session.session_number} ({self.status})"
