from django import forms
from .models import Project, ProjectSubmission

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'course',
            'course_session',
            'title',
            'description',
            'instructions',
            'deadline',
            'max_score',
            'status'
        ]
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control default-select wide'}),
            'course_session': forms.Select(attrs={'class': 'form-control default-select wide'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul Project'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Deskripsi Project'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Petunjuk Pengerjaan'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'max_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control default-select wide'}),
        }
        labels = {
            'course': 'Program Les',
            'course_session': 'Sesi Pertemuan',
            'title': 'Judul Project',
            'description': 'Deskripsi',
            'instructions': 'Petunjuk',
            'deadline': 'Tenggat Waktu',
            'max_score': 'Skor Maksimal',
            'status': 'Status',
        }


class ProjectSubmissionForm(forms.ModelForm):
    class Meta:
        model = ProjectSubmission
        fields = [
            'submission_type',
            'file',
            'link',
            'description',
        ]
        widgets = {
            'submission_type': forms.Select(attrs={'class': 'form-control default-select wide'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/username/repository atau link demo'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Keterangan tambahan...'}),
        }
        labels = {
            'submission_type': 'Tipe Pengumpulan',
            'file': 'File Tugas',
            'link': 'Link Tugas',
            'description': 'Deskripsi/Catatan',
        }


class ProjectReviewForm(forms.ModelForm):
    class Meta:
        model = ProjectSubmission
        fields = [
            'score',
            'feedback',
            'status',
        ]
        widgets = {
            'score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Nilai'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Catatan feedback untuk siswa'}),
            'status': forms.Select(attrs={'class': 'form-control default-select wide'}),
        }
        labels = {
            'score': 'Nilai',
            'feedback': 'Feedback',
            'status': 'Status Kelulusan',
        }
