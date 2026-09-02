from django import forms
from .models import Course, CourseEnrollment, CourseSession, CourseTeacher
from tutors.models import Teacher

class CourseForm(forms.ModelForm):
    teachers = forms.ModelMultipleChoiceField(
        queryset=Teacher.objects.filter(status='ACTIVE'),
        required=False,
        label='Tutor / Pengajar Les',
        widget=forms.SelectMultiple(attrs={'class': 'form-control default-select wide'}),
        help_text='Pilih satu atau lebih Tutor yang mengajar kelas/program les ini'
    )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['teachers'].initial = Teacher.objects.filter(course_teachers__course=self.instance)

    def save(self, commit=True):
        course = super().save(commit=commit)
        if commit:
            selected_teachers = self.cleaned_data.get('teachers', [])
            CourseTeacher.objects.filter(course=course).delete()
            for teacher in selected_teachers:
                CourseTeacher.objects.create(course=course, teacher=teacher, role='Primary Tutor')
        return course


class CourseEnrollmentForm(forms.ModelForm):
    class Meta:
        model = CourseEnrollment
        fields = ['course', 'student', 'status']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control default-select wide', 'id': 'id_course'}),
            'student': forms.Select(attrs={'class': 'form-control default-select wide', 'id': 'id_student'}),
            'status': forms.Select(attrs={'class': 'form-control default-select wide'}),
        }
        labels = {
            'course': 'Program Les',
            'student': 'Siswa',
            'status': 'Status Keanggotaan',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from students.models import Student
        from django.db.models import Q
        
        enrolled_student_ids = CourseEnrollment.objects.values_list('student_id', flat=True)
        
        if self.instance and self.instance.pk:
            self.fields['student'].queryset = Student.objects.filter(
                Q(pk=self.instance.student_id) | ~Q(pk__in=enrolled_student_ids)
            ).select_related('user')
        else:
            self.fields['student'].queryset = Student.objects.exclude(
                pk__in=enrolled_student_ids
            ).select_related('user')

    def clean(self):
        cleaned_data = super().clean()
        course = cleaned_data.get('course')
        student = cleaned_data.get('student')
        
        if course and student:
            existing = CourseEnrollment.objects.filter(course=course, student=student)
            if self.instance and self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise forms.ValidationError(f"Siswa {student} sudah terdaftar di program les '{course.name}'.")
        return cleaned_data


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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.role in ['TUTOR', 'GURU'] and hasattr(user, 'teacher_profile'):
            teacher_profile = user.teacher_profile
            assigned_courses = Course.objects.filter(course_teachers__teacher=teacher_profile)
            if assigned_courses.exists():
                self.fields['course'].queryset = assigned_courses
            self.fields['teacher'].initial = teacher_profile

