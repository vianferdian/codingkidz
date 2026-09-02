from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class CompleteProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and getattr(request.user, 'role', '') == 'STUDENT':
            student = getattr(request.user, 'student_profile', None)
            if student:
                # Profile is incomplete if school_name or parent_phone or gender is missing
                is_incomplete = (
                    not student.school_name or 
                    not student.parent_phone or 
                    not (student.gender or request.user.gender)
                )
                if is_incomplete:
                    edit_url = reverse('getskills:edit-user', kwargs={'id': request.user.id})
                    current_path = request.path
                    
                    # If user tries to go to any page other than edit profile/logout/static/admin, redirect once with message
                    if not (current_path == edit_url or 
                            current_path.startswith('/logout') or 
                            current_path.startswith('/accounts/') or
                            current_path.startswith('/static/') or 
                            current_path.startswith('/media/') or
                            current_path.startswith('/admin/')):
                        messages.warning(request, "Silakan lengkapi data diri Anda (Nama Sekolah, No. WA Orang Tua, Jenis Kelamin) sebelum mengakses dashboard.")
                        return redirect(edit_url)
                        
        response = self.get_response(request)
        return response
