from django.contrib.auth.backends import ModelBackend
from users.models import CustomUser
from students.models import Student

class EmailOrStudentCodeBackend(ModelBackend):
    """
    Custom authentication backend that allows users to authenticate
    using either their Email address or Student Code (Kode Siswa).
    """
    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        login_id = username or email or kwargs.get('login_input')
        if not login_id or not password:
            return None

        user = None
        login_id = login_id.strip()

        # 1. Try finding CustomUser by email (case-insensitive)
        try:
            user = CustomUser.objects.get(email__iexact=login_id)
        except CustomUser.DoesNotExist:
            # 2. Try finding Student by student_code (case-insensitive)
            try:
                student = Student.objects.get(student_code__iexact=login_id)
                user = student.user
            except Student.DoesNotExist:
                return None

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
