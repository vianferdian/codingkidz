from django import forms
from django.core.exceptions import ValidationError
from users.models import CustomUser
from .models import Teacher

class TeacherForm(forms.ModelForm):
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
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label="Tanggal Lahir")

    class Meta:
        model = Teacher
        fields = [
            'type',
            'specialization',
            'phone',
            'status',
        ]
        labels = {
            'type': 'Tipe Pengajar',
            'specialization': 'Spesialisasi / Keahlian',
            'phone': 'No. Telepon',
            'status': 'Status',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email ini sudah terdaftar.")
        return email

    def save(self, commit=True):
        teacher = super().save(commit=False)
        
        # Create user
        user = CustomUser.objects.create_user(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            role=self.cleaned_data['type'],  # Set role to TUTOR or GURU depending on selected type
            gender=self.cleaned_data['gender'],
            dob=self.cleaned_data['dob'].strftime('%d-%m-%Y') if self.cleaned_data.get('dob') else '',
            phone_number=self.cleaned_data.get('phone') or '',
            is_active=True
        )
        
        if self.cleaned_data.get('avatar'):
            user.avatar = self.cleaned_data['avatar']
            user.save()
            
        teacher.user = user
        if commit:
            teacher.save()
        return teacher


class TeacherEditForm(forms.ModelForm):
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
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label="Tanggal Lahir")

    class Meta:
        model = Teacher
        fields = [
            'type',
            'specialization',
            'phone',
            'status',
        ]
        labels = {
            'type': 'Tipe Pengajar',
            'specialization': 'Spesialisasi / Keahlian',
            'phone': 'No. Telepon',
            'status': 'Status',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['gender'].initial = self.instance.user.gender
            # parse dob if exists
            if self.instance.user.dob:
                from datetime import datetime
                try:
                    self.fields['dob'].initial = datetime.strptime(self.instance.user.dob, '%d-%m-%Y').date()
                except:
                    pass

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.user.email
        if email != current_email and CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email ini sudah terdaftar.")
        return email

    def save(self, commit=True):
        teacher = super().save(commit=False)
        user = teacher.user
        
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.gender = self.cleaned_data['gender']
        user.role = self.cleaned_data['type']  # Sync role with teacher type
        if self.cleaned_data.get('dob'):
            user.dob = self.cleaned_data['dob'].strftime('%d-%m-%Y')
        user.phone_number = self.cleaned_data.get('phone') or ''
        
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
            
        if self.cleaned_data.get('avatar'):
            user.avatar = self.cleaned_data['avatar']
            
        user.save()
        
        if commit:
            teacher.save()
        return teacher
