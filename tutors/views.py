from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.decorators import role_required
from .models import Teacher
from .forms import TeacherForm, TeacherEditForm

@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def teacher_list(request):
    # Filter by query param for tutor vs guru
    role_type = request.GET.get('type')
    if role_type:
        teachers = Teacher.objects.filter(type=role_type.upper()).order_by('-created_at')
        title = f"Manajemen {role_type.capitalize()}"
    else:
        teachers = Teacher.objects.all().order_by('-created_at')
        title = "Manajemen Pengajar (Tutor & Guru)"
        
    context = {
        "teachers": teachers,
        "page_title": title,
        "role_type": role_type
    }
    return render(request, 'tutors/teacher_list.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def add_teacher(request):
    role_type = request.GET.get('type', 'tutor')
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f'Pengajar {teacher.user.first_name} {teacher.user.last_name} berhasil ditambahkan.')
            return redirect(f"/tutors/list/?type={teacher.type.lower()}")
    else:
        form = TeacherForm(initial={'type': role_type.upper()})
    
    context = {
        'form': form,
        'page_title': f'Tambah {role_type.capitalize()}',
        'is_add': True
    }
    return render(request, 'tutors/teacher_form.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        form = TeacherEditForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f'Pengajar {teacher.user.first_name} {teacher.user.last_name} berhasil diperbarui.')
            return redirect(f"/tutors/list/?type={teacher.type.lower()}")
    else:
        form = TeacherEditForm(instance=teacher)
    
    context = {
        'form': form,
        'teacher': teacher,
        'page_title': f'Edit Pengajar - {teacher.user.first_name} {teacher.user.last_name}',
        'is_add': False
    }
    return render(request, 'tutors/teacher_form.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    user = teacher.user
    teacher_type = teacher.type.lower() if teacher.type else 'tutor'
    full_name = f"{user.first_name} {user.last_name}".strip() if user else "Pengajar"
    teacher.delete()
    if user:
        user.delete()
    messages.success(request, f"Data pengajar {full_name} dan akun terkait berhasil dihapus.")
    return redirect(f"/tutors/list/?type={teacher_type}")

