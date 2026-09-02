from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.decorators import role_required
from .models import Student
from .forms import StudentForm, StudentEditForm, StudentRegistrationForm

@login_required(login_url='getskills:login')
@role_required(['ADMIN', 'GURU'])
def student_list(request):
    students = Student.objects.all().order_by('-created_at')
    context = {
        "students": students,
        "page_title": "Manajemen Siswa"
    }
    return render(request, 'students/student_list.html', context)


def register_student(request):
    if request.user.is_authenticated:
        return redirect('getskills:index')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(
                request, 
                f'Registrasi berhasil! Kode Siswa Anda adalah: {student.student_code}. Silakan masuk menggunakan Email atau Kode Siswa.'
            )
            return redirect('getskills:login')
        else:
            messages.error(request, 'Terjadi kesalahan pada pengisian form. Silakan periksa kembali data Anda.')
    else:
        form = StudentRegistrationForm()

    context = {
        'form': form,
        'page_title': 'Registrasi Siswa Baru'
    }
    return render(request, 'students/student_register.html', context)



@login_required(login_url='getskills:login')
@role_required(['ADMIN', 'GURU'])
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Siswa {student.user.first_name} {student.user.last_name} berhasil ditambahkan.')
            return redirect('students:student_list')
    else:
        form = StudentForm()
    
    context = {
        'form': form,
        'page_title': 'Tambah Siswa'
    }
    return render(request, 'students/student_add.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN', 'GURU'])
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentEditForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Siswa {student.user.first_name} {student.user.last_name} berhasil diperbarui.')
            return redirect('students:student_list')
    else:
        form = StudentEditForm(instance=student)
    
    context = {
        'form': form,
        'student': student,
        'page_title': 'Edit Siswa'
    }
    return render(request, 'students/student_edit.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = student.user
    full_name = f"{user.first_name} {user.last_name}".strip() or user.username
    student.delete()
    if user:
        user.delete()
    messages.success(request, f"Data siswa {full_name} dan akun terkait berhasil dihapus.")
    return redirect('students:student_list')

