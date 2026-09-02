from django import forms
from django.core.exceptions import ValidationError
from users.models import CustomUser
from .models import Student

class StudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True, label="Nama Depan")
    last_name = forms.CharField(max_length=150, required=True, label="Nama Belakang")
    email = forms.EmailField(required=True, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")
    avatar = forms.ImageField(required=False, label="Foto Profil", widget=forms.FileInput(attrs={'id': 'id_avatar', 'accept': 'image/*'}))

    
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
    avatar = forms.ImageField(required=False, label="Foto Profil", widget=forms.FileInput(attrs={'id': 'id_avatar', 'accept': 'image/*'}))

    
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
        if 'status' in self.fields:
            self.fields['status'].required = False
        if 'student_code' in self.fields:
            self.fields['student_code'].required = False
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['gender'].initial = self.instance.user.gender or self.instance.gender
            self.fields['birth_date'].initial = self.instance.birth_date


    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.user.email
        if email != current_email and CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email ini sudah terdaftar.")
        return email

    def clean_student_code(self):
        student_code = self.cleaned_data.get('student_code')
        if not student_code and self.instance and self.instance.student_code:
            return self.instance.student_code
        current_code = self.instance.student_code if self.instance else None
        if student_code and student_code != current_code and Student.objects.filter(student_code=student_code).exists():
            raise ValidationError("Kode siswa ini sudah digunakan.")
        return student_code or current_code

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if not status and self.instance and self.instance.status:
            return self.instance.status
        return status or (self.instance.status if self.instance else 'ACTIVE')



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


def generate_memorable_student_code(first_name, last_name):
    import random
    fn = (first_name or '').strip().upper()
    ln = (last_name or '').strip().upper()
    
    fn_initial = fn[0] if fn else 'S'
    ln_initial = ln[0] if ln else (fn[1] if len(fn) > 1 else 'T')
    
    prefix = f"CK-{fn_initial}{ln_initial}"
    
    while True:
        rand_num = random.randint(1000, 9999)
        code = f"{prefix}{rand_num}"
        if not Student.objects.filter(student_code=code).exists():
            return code


class StudentRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True, label="Nama Depan")
    last_name = forms.CharField(max_length=150, required=True, label="Nama Belakang")
    email = forms.EmailField(required=True, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")
    avatar = forms.ImageField(required=False, label="Foto Profil", widget=forms.FileInput(attrs={'id': 'id_avatar', 'accept': 'image/*'}))

    
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
            'school_name',
            'parent_name',
            'parent_phone',
            'birth_date',
            'gender',
            'address',
        ]
        labels = {
            'school_name': 'Nama Sekolah',
            'parent_name': 'Nama Orang Tua',
            'parent_phone': 'No. Telp Orang Tua',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email ini sudah terdaftar.")
        return email

    def save(self, commit=True):
        student = super().save(commit=False)
        student.status = 'ACTIVE'
        student.student_code = generate_memorable_student_code(
            self.cleaned_data.get('first_name'),
            self.cleaned_data.get('last_name')
        )
        
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

