from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.decorators import role_required
from .models import Course, CourseEnrollment, CourseSession
from .forms import CourseForm, CourseEnrollmentForm, CourseSessionForm

@login_required(login_url='getskills:login')
def course_list(request):
    courses = Course.objects.all().order_by('name')
    context = {
        "courses": courses,
        "page_title": "Program Les"
    }
    return render(request, 'academics/course_list.html', context)

@login_required(login_url='getskills:login')
def class_list(request):
    role = request.user.role
    
    if role == 'STUDENT':
        enrollments = CourseEnrollment.objects.filter(student__user=request.user)
        context = {"enrollments": enrollments, "page_title": "Kelas Saya"}
        return render(request, 'academics/student_class_list.html', context)
    elif role in ['TUTOR', 'GURU']:
        my_courses = Course.objects.filter(
            models.Q(course_teachers__teacher__user=request.user) |
            models.Q(sessions__teacher__user=request.user)
        ).distinct().order_by('name')
        
        enrollments = CourseEnrollment.objects.filter(
            course__in=my_courses
        ).distinct().order_by('-joined_at')
        
        context = {
            "courses": my_courses,
            "enrollments": enrollments,
            "page_title": "Kelas Saya"
        }
        return render(request, 'academics/teacher_class_list.html', context)
    else:
        # Admin: show all enrollments
        enrollments = CourseEnrollment.objects.all().order_by('-joined_at')
        context = {"enrollments": enrollments, "page_title": "Manajemen Kelas & Pendaftaran"}
        return render(request, 'academics/admin_class_list.html', context)


from django.db import models

@login_required(login_url='getskills:login')
def session_list(request):
    role = request.user.role
    if role in ['TUTOR', 'GURU'] and hasattr(request.user, 'teacher_profile'):
        teacher_profile = request.user.teacher_profile
        sessions = CourseSession.objects.filter(
            models.Q(teacher=teacher_profile) | 
            models.Q(course__course_teachers__teacher=teacher_profile)
        ).distinct().order_by('session_date', 'start_time')
    else:
        sessions = CourseSession.objects.all().order_by('session_date', 'start_time')

    context = {
        "sessions": sessions,
        "page_title": "Pertemuan Sesi Belajar"
    }
    return render(request, 'academics/session_list.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, f"Program Les '{course.name}' berhasil ditambahkan.")
            return redirect('academics:course_list')
    else:
        form = CourseForm()
        
    context = {
        'form': form,
        'page_title': 'Tambah Program Les Baru',
        'cancel_url': '/academics/course/'
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def add_enrollment(request):
    if request.method == 'POST':
        form = CourseEnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save()
            messages.success(request, f"Siswa '{enrollment.student}' berhasil didaftarkan ke kelas '{enrollment.course}'.")
            return redirect('academics:class_list')
    else:
        form = CourseEnrollmentForm()

    import json
    enrolled_data = {}
    for e in CourseEnrollment.objects.exclude(status='INACTIVE').values('course_id', 'student_id'):
        cid = str(e['course_id'])
        if cid not in enrolled_data:
            enrolled_data[cid] = []
        enrolled_data[cid].append(e['student_id'])
        
    context = {
        'form': form,
        'page_title': 'Daftarkan Siswa ke Program/Kelas',
        'cancel_url': '/academics/class/',
        'enrolled_mapping_json': json.dumps(enrolled_data)
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def edit_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(CourseEnrollment, id=enrollment_id)
    if request.method == 'POST':
        form = CourseEnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            messages.success(request, "Pendaftaran siswa berhasil diperbarui.")
            return redirect('academics:class_list')
    else:
        form = CourseEnrollmentForm(instance=enrollment)
        
    context = {
        'form': form,
        'page_title': 'Edit Pendaftaran Kelas',
        'cancel_url': '/academics/class/'
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN', 'TUTOR', 'GURU'])
def add_session(request):
    user_teacher = getattr(request.user, 'teacher_profile', None)
    if request.method == 'POST':
        form = CourseSessionForm(request.POST, user=request.user)
        if form.is_valid():
            session = form.save(commit=False)
            if user_teacher and not session.teacher:
                session.teacher = user_teacher
            session.save()
            messages.success(request, f"Jadwal Sesi Pertemuan #{session.session_number} ({session.course}) berhasil dibuat.")
            return redirect('academics:session_list')
    else:
        form = CourseSessionForm(user=request.user)
        
    context = {
        'form': form,
        'page_title': 'Tambah Jadwal Sesi Pertemuan',
        'cancel_url': '/academics/session/'
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN', 'TUTOR', 'GURU'])
def edit_session(request, session_id):
    session = get_object_or_404(CourseSession, id=session_id)
    if request.method == 'POST':
        form = CourseSessionForm(request.POST, instance=session, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Jadwal sesi pertemuan berhasil diperbarui.")
            return redirect('academics:session_list')
    else:
        form = CourseSessionForm(instance=session, user=request.user)
        
    context = {
        'form': form,
        'page_title': f"Edit Sesi Pertemuan - #{session.session_number} {session.course.name}",
        'cancel_url': '/academics/session/'
    }
    return render(request, 'projects/project_form.html', context)



@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f"Program Les '{course.name}' berhasil diperbarui.")
            return redirect('academics:course_list')
    else:
        form = CourseForm(instance=course)
        
    context = {
        'form': form,
        'page_title': 'Edit Program Les',
        'cancel_url': '/academics/courses/'
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    name = course.name
    course.delete()
    messages.success(request, f"Program Les '{name}' berhasil dihapus.")
    return redirect('academics:course_list')


@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def delete_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(CourseEnrollment, id=enrollment_id)
    student = enrollment.student
    course = enrollment.course
    enrollment.delete()
    messages.success(request, f"Pendaftaran '{student}' dari kelas '{course}' berhasil dihapus.")
    return redirect('academics:class_list')


@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def delete_session(request, session_id):
    session = get_object_or_404(CourseSession, id=session_id)
    session_num = session.session_number
    course_name = session.course.name
    session.delete()
    messages.success(request, f"Sesi Pertemuan #{session_num} dari kelas '{course_name}' berhasil dihapus.")
    return redirect('academics:session_list')
