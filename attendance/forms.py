from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = [
            'course_session',
            'student',
            'status',
            'check_in_at',
            'notes',
        ]
        widgets = {
            'course_session': forms.Select(attrs={'class': 'form-control default-select wide'}),
            'student': forms.Select(attrs={'class': 'form-control default-select wide'}),
            'status': forms.Select(attrs={'class': 'form-control default-select wide'}),
            'check_in_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Catatan kehadiran...'}),
        }
        labels = {
            'course_session': 'Sesi Kelas',
            'student': 'Siswa',
            'status': 'Status Kehadiran',
            'check_in_at': 'Waktu Absen',
            'notes': 'Catatan',
        }
