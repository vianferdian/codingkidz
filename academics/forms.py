from django import forms
from .models import Course, CourseEnrollment, CourseSession

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name', 'description', 'price', 'total_sessions', 'status']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kode Program (cth: CODE-01)'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Program'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Deskripsi Program'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'total_sessions': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control default-select wide'}),
        }
        labels = {
            'code': 'Kode Program',
            'name': 'Nama Program',
            'description': 'Deskripsi',
            'price': 'Harga / Biaya',
            'total_sessions': 'Jumlah Pertemuan',
            'status': 'Status',
        }


class CourseEnrollmentForm(forms.ModelForm):
    class Meta:
        model = CourseEnrollment
        fields = ['course', 'student', 'status']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control default-select wide'}),
            'student': forms.Select(attrs={'class': 'form-control default-select wide'}),
            'status': forms.Select(attrs={'class': 'form-control default-select wide'}),
        }
        labels = {
            'course': 'Program Les',
            'student': 'Siswa',
            'status': 'Status Keanggotaan',
        }


class CourseSessionForm(forms.ModelForm):
    class Meta:
        model = CourseSession
        fields = [
            'course',
            'session_number',
            'title',
            'session_date',
            'start_time',
            'end_time',
            'teacher',
            'room',
            'material',
            'status'
        ]
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control default-select wide'}),
            'session_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Topik / Judul Pertemuan'}),
            'session_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control default-select wide'}),
            'room': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Ruangan'}),
            'material': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Materi Pembelajaran'}),
            'status': forms.Select(attrs={'class': 'form-control default-select wide'}),
        }
        labels = {
            'course': 'Program Les',
            'session_number': 'Pertemuan Sesi Ke-',
            'title': 'Judul Sesi',
            'session_date': 'Tanggal',
            'start_time': 'Waktu Mulai',
            'end_time': 'Waktu Selesai',
            'teacher': 'Pengajar (Guru/Tutor)',
            'room': 'Ruangan Kelas',
            'material': 'Materi',
            'status': 'Status',
        }
