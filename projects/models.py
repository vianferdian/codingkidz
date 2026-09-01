from django.db import models
from django.conf import settings
from academics.models import Course, CourseSession
from students.models import Student
from tutors.models import Teacher

class Project(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('ARCHIVED', 'Archived'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='projects')
    course_session = models.ForeignKey(CourseSession, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField()
    max_score = models.IntegerField(default=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_projects')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.course.name})"

class ProjectSubmission(models.Model):
    STATUS_CHOICES = (
        ('SUBMITTED', 'Submitted'),
        ('LATE', 'Submitted Late'),
        ('REVIEWED', 'Reviewed'),
        ('REVISION_REQUIRED', 'Revision Required'),
        ('COMPLETED', 'Completed / Approved'),
    )
    TYPE_CHOICES = (
        ('FILE', 'File Upload'),
        ('LINK', 'URL Link'),
        ('BOTH', 'File and URL Link'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    submission_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='FILE')
    file = models.FileField(upload_to='project_submissions/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='SUBMITTED')
    score = models.IntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_submissions')
    reviewed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('project', 'student')

    def __str__(self):
        return f"{self.student.user.first_name} -> {self.project.title} ({self.status})"
