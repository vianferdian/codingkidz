from django import forms
from django.core.exceptions import ValidationError
from users.models import CustomUser
from .models import Student

class StudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True, label="Nama Depan")
    last_name = forms.CharField(max_length=150, required=True, label="Nama Belakang")
    email = forms.EmailField(required=True, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")
    avatar = forms.ImageField(required=False, label="Foto Profil")
    
    GENDER_CHOICES = (
        ('', 'Pilih Jenis Kelamin'),
        ('Male', 'Laki-laki'),
        ('Female', 'Perempuan'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True, label="Jenis Kelamin")
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label="Tanggal Lahir")
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label="Alamat")

    class Meta:
        model = Student
        fields = [
            'student_code',
            'school_name',
            'parent_name',
            'parent_phone',
            'birth_date',
            'gender',
            'address',
            'status',
        ]
        labels = {
            'student_code': 'Kode Siswa',
            'school_name': 'Nama Sekolah',
            'parent_name': 'Nama Orang Tua',
            'parent_phone': 'No. Telp Orang Tua',
            'status': 'Status',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email ini sudah terdaftar.")
        return email

    def clean_student_code(self):
        student_code = self.cleaned_data.get('student_code')
        if Student.objects.filter(student_code=student_code).exists():
            raise ValidationError("Kode siswa ini sudah digunakan.")
        return student_code

    def save(self, commit=True):
        student = super().save(commit=False)
        
        # Create user
        user = CustomUser.objects.create_user(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            role='STUDENT',
            gender=self.cleaned_data['gender'],
            dob=self.cleaned_data['birth_date'].strftime('%d-%m-%Y') if self.cleaned_data.get('birth_date') else '',
            phone_number=self.cleaned_data.get('parent_phone') or '',
            is_active=True
        )
        
        if self.cleaned_data.get('avatar'):
            user.avatar = self.cleaned_data['avatar']
            user.save()
            
        student.user = user
        if commit:
            student.save()
        return student


class StudentEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True, label="Nama Depan")
    last_name = forms.CharField(max_length=150, required=True, label="Nama Belakang")
    email = forms.EmailField(required=True, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="Password Baru (Kosongkan jika tidak diubah)")
    avatar = forms.ImageField(required=False, label="Foto Profil")
    
    GENDER_CHOICES = (
        ('', 'Pilih Jenis Kelamin'),
        ('Male', 'Laki-laki'),
        ('Female', 'Perempuan'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True, label="Jenis Kelamin")
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label="Tanggal Lahir")
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label="Alamat")

    class Meta:
        model = Student
        fields = [
            'student_code',
            'school_name',
            'parent_name',
            'parent_phone',
            'birth_date',
            'gender',
            'address',
            'status',
        ]
        labels = {
            'student_code': 'Kode Siswa',
            'school_name': 'Nama Sekolah',
            'parent_name': 'Nama Orang Tua',
            'parent_phone': 'No. Telp Orang Tua',
            'status': 'Status',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['gender'].initial = self.instance.user.gender
            # Keep avatar field as is (ImageField handles it)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.user.email
        if email != current_email and CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email ini sudah terdaftar.")
        return email

    def clean_student_code(self):
        student_code = self.cleaned_data.get('student_code')
        current_code = self.instance.student_code
        if student_code != current_code and Student.objects.filter(student_code=student_code).exists():
            raise ValidationError("Kode siswa ini sudah digunakan.")
        return student_code

    def save(self, commit=True):
        student = super().save(commit=False)
        user = student.user
        
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.gender = self.cleaned_data['gender']
        if self.cleaned_data.get('birth_date'):
            user.dob = self.cleaned_data['birth_date'].strftime('%d-%m-%Y')
        user.phone_number = self.cleaned_data.get('parent_phone') or ''
        
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
            
        if self.cleaned_data.get('avatar'):
            user.avatar = self.cleaned_data['avatar']
            
        user.save()
        
        if commit:
            student.save()
        return student
