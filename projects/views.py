from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from users.decorators import role_required
from .models import Project, ProjectSubmission
from .forms import ProjectForm, ProjectSubmissionForm, ProjectReviewForm
from students.models import Student
from users.models import CustomUser
from notifications.utils import create_notification

@login_required(login_url='getskills:login')
def project_list(request):
    role = request.user.role
    
    if role == 'STUDENT':
        projects = Project.objects.filter(course__enrollments__student__user=request.user, status='ACTIVE').order_by('-deadline')
        context = {"projects": projects, "page_title": "Project Les Saya"}
        return render(request, 'projects/student_project_list.html', context)
    else:
        projects = Project.objects.all().order_by('-deadline')
        context = {"projects": projects, "page_title": "Daftar Project / Tugas"}
        return render(request, 'projects/project_list.html', context)

@login_required(login_url='getskills:login')
def submission_list(request):
    role = request.user.role
    
    if role == 'STUDENT':
        submissions = ProjectSubmission.objects.filter(student__user=request.user).order_by('-submitted_at')
        context = {"submissions": submissions, "page_title": "Riwayat Tugas Saya"}
        return render(request, 'projects/student_submission_list.html', context)
    else:
        submissions = ProjectSubmission.objects.all().order_by('-submitted_at')
        context = {"submissions": submissions, "page_title": "Daftar Submission Tugas Siswa"}
        return render(request, 'projects/submission_list.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN', 'GURU'])
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            
            # Notify enrolled students
            students = Student.objects.filter(enrollments__course=project.course, enrollments__status='ACTIVE')
            for s in students:
                create_notification(
                    user=s.user,
                    title="Project / Tugas Baru Ditugaskan",
                    message=f"Tugas baru '{project.title}' telah ditugaskan untuk Kelas {project.course.name}. Batas waktu: {project.deadline.strftime('%d-%m-%Y %H:%M')}",
                    notification_type='PROJECT'
                )
                
            messages.success(request, f"Project '{project.title}' berhasil dibuat.")
            return redirect('projects:project_list')
    else:
        form = ProjectForm()
        
    context = {
        'form': form,
        'page_title': 'Buat Project Baru',
        'cancel_url': '/projects/list/'
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN', 'GURU'])
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(request, f"Project '{project.title}' berhasil diperbarui.")
            return redirect('projects:project_list')
    else:
        form = ProjectForm(instance=project)
        
    context = {
        'form': form,
        'page_title': f"Edit Project - {project.title}",
        'cancel_url': '/projects/list/'
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='getskills:login')
@role_required(['STUDENT'])
def submit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    student_profile = request.user.student_profile
    
    submission = ProjectSubmission.objects.filter(project=project, student=student_profile).first()
    
    if request.method == 'POST':
        form = ProjectSubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            new_sub = form.save(commit=False)
            new_sub.project = project
            new_sub.student = student_profile
            if timezone.now() > project.deadline:
                new_sub.status = 'LATE'
            else:
                new_sub.status = 'SUBMITTED'
            new_sub.save()
            
            # Notify Admin
            admins = CustomUser.objects.filter(role='ADMIN')
            for admin in admins:
                create_notification(
                    user=admin,
                    title="Tugas Baru Dikumpulkan",
                    message=f"Siswa {student_profile.user.first_name} {student_profile.user.last_name} mengumpulkan tugas '{project.title}' untuk Kelas {project.course.name}.",
                    notification_type='PROJECT'
                )
                
            messages.success(request, "Tugas/Project berhasil dikumpulkan.")
            return redirect('projects:submission_list')
    else:
        form = ProjectSubmissionForm(instance=submission)
        
    context = {
        'form': form,
        'page_title': f"Kumpulkan Tugas: {project.title}",
        'cancel_url': '/projects/list/'
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN', 'GURU', 'TUTOR'])
def review_submission(request, submission_id):
    submission = get_object_or_404(ProjectSubmission, id=submission_id)
    if request.method == 'POST':
        form = ProjectReviewForm(request.POST, instance=submission)
        if form.is_valid():
            review = form.save(commit=False)
            # Find teacher profile if role is GURU or TUTOR
            if hasattr(request.user, 'teacher_profile'):
                review.reviewed_by = request.user.teacher_profile
            review.reviewed_at = timezone.now()
            review.save()
            
            # Notify Student
            if review.status == 'REVISION_REQUIRED':
                create_notification(
                    user=submission.student.user,
                    title="Tugas Perlu Revisi",
                    message=f"Tugas '{submission.project.title}' Anda memerlukan revisi. Feedback: '{review.feedback or '-'}'. Silakan perbaiki dan kirim ulang.",
                    notification_type='PROJECT'
                )
            else:
                create_notification(
                    user=submission.student.user,
                    title="Tugas Selesai Dinilai",
                    message=f"Tugas '{submission.project.title}' Anda telah dinilai. Nilai: {review.score or 0}/{submission.project.max_score}. Feedback: '{review.feedback or '-'}'.",
                    notification_type='PROJECT'
                )
                
            messages.success(request, f"Submission {submission.student.user.first_name} berhasil dinilai.")
            return redirect('projects:submission_list')
    else:
        form = ProjectReviewForm(instance=submission)
        
    context = {
        'form': form,
        'submission': submission,
        'page_title': f"Review & Nilai Tugas - {submission.student.user.first_name} {submission.student.user.last_name}",
        'cancel_url': '/projects/submissions/'
    }
    return render(request, 'projects/project_form.html', context)
