from django.db import models
from students.models import Student
from tutors.models import Teacher

class Course(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    )
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    total_sessions = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class CourseEnrollment(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    joined_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')

    class Meta:
        unique_together = ('course', 'student')

    def __str__(self):
        return f"{self.student} -> {self.course}"

class CourseTeacher(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_teachers')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='course_teachers')
    role = models.CharField(max_length=100, blank=True, null=True, default='Primary Tutor')

    class Meta:
        unique_together = ('course', 'teacher')

    def __str__(self):
        return f"{self.teacher} in {self.course} ({self.role})"

class CourseSession(models.Model):
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions')
    session_number = models.IntegerField()
    title = models.CharField(max_length=255, blank=True, null=True)
    session_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions')
    room = models.CharField(max_length=100, blank=True, null=True, default='Classroom')
    material = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.name} - Session #{self.session_number} ({self.session_date})"
