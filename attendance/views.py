from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from users.decorators import role_required
from .models import Attendance
from .forms import AttendanceForm
from academics.models import CourseSession
from students.models import Student

@login_required(login_url='getskills:login')
def attendance_list(request):
    role = request.user.role
    
    if role == 'STUDENT':
        attendances = Attendance.objects.filter(student__user=request.user).order_by('-course_session__session_date')
        context = {"attendances": attendances, "page_title": "Riwayat Kehadiran Saya"}
        return render(request, 'attendance/student_attendance_list.html', context)
    elif role in ['TUTOR', 'GURU']:
        attendances = Attendance.objects.filter(course_session__teacher__user=request.user).order_by('-course_session__session_date')
        tutor_sessions = CourseSession.objects.filter(teacher__user=request.user).select_related('course').order_by('-session_date', '-start_time')
        context = {
            "attendances": attendances,
            "tutor_sessions": tutor_sessions,
            "page_title": "Manajemen Presensi Kelas"
        }
        return render(request, 'attendance/teacher_attendance_list.html', context)
    else:
        # Admin
        attendances = Attendance.objects.all().order_by('-course_session__session_date')
        context = {"attendances": attendances, "page_title": "Laporan & Log Kehadiran"}
        return render(request, 'attendance/admin_attendance_list.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN', 'TUTOR'])
def tutor_take_attendance(request, session_id):
    course_session = get_object_or_404(CourseSession, id=session_id)
    
    # Keamanan: pastikan tutor yang login adalah tutor yang mengajar sesi ini (atau Admin)
    if request.user.role != 'ADMIN' and (not course_session.teacher or course_session.teacher.user != request.user):
        messages.error(request, "Anda tidak memiliki akses ke sesi ini.")
        return redirect('attendance:attendance_list')
        
    # Ambil semua siswa yang terdaftar di kelas/course sesi ini
    students = Student.objects.filter(enrollments__course=course_session.course, enrollments__status='ACTIVE').select_related('user')
    
    # Ambil absensi yang sudah tercatat
    attendances = Attendance.objects.filter(course_session=course_session)
    attendance_dict = {att.student_id: att.status for att in attendances}
    
    context = {
        "page_title": f"Presensi: {course_session.course.name} - Sesi #{course_session.session_number}",
        "course_session": course_session,
        "students": students,
        "attendance_dict": attendance_dict,
    }
    return render(request, 'attendance/tutor_take_attendance.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN', 'TUTOR'])
def tutor_submit_attendance_ajax(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        student_id = request.POST.get('student_id')
        status = request.POST.get('status')  # 'HADIR' atau 'ALPA'/'IZIN'/'SAKIT'
        
        course_session = get_object_or_404(CourseSession, id=session_id)
        student = get_object_or_404(Student, id=student_id)
        
        # Keamanan: pastikan tutor yang login adalah pengajar sesi ini (atau Admin)
        if request.user.role != 'ADMIN' and (not course_session.teacher or course_session.teacher.user != request.user):
            return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)
            
        attendance, created = Attendance.objects.get_or_create(
            course_session=course_session,
            student=student,
            defaults={'status': status, 'recorded_by': request.user, 'check_in_at': timezone.now()}
        )
        
        if not created:
            attendance.status = status
            attendance.recorded_by = request.user
            attendance.check_in_at = timezone.now()
            attendance.save()
            
        return JsonResponse({"status": "success", "message": f"Kehadiran {student.user.first_name} diperbarui ke {status}."})
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


@login_required(login_url='getskills:login')
@role_required(['ADMIN', 'TUTOR'])
def add_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.recorded_by = request.user
            attendance.save()
            messages.success(request, "Data kehadiran berhasil dicatat.")
            return redirect('attendance:attendance_list')
    else:
        form = AttendanceForm(initial={'check_in_at': timezone.now()})
        
    context = {
        'form': form,
        'page_title': 'Isi Presensi Kehadiran',
        'cancel_url': '/attendance/list/'
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN', 'TUTOR'])
def edit_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, "Data kehadiran berhasil diperbarui.")
            return redirect('attendance:attendance_list')
    else:
        form = AttendanceForm(instance=attendance)
        
    context = {
        'form': form,
        'page_title': 'Edit Presensi Kehadiran',
        'cancel_url': '/attendance/list/'
    }
    return render(request, 'projects/project_form.html', context)
