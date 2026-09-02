import sys
import traceback
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from students.models import Student
from students.forms import generate_memorable_student_code

class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return True

    def clean_username(self, username, shallow=False):
        return None

    def populate_username(self, request, user):
        pass


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def on_authentication_error(self, request, provider, error=None, exception=None, extra_context=None):
        err_msg = f"=== OAUTH ERROR ===\nGET: {dict(request.GET)}\nError: {error}\nException: {exception}\n"
        if exception:
            err_msg += "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        err_msg += "===================\n"
        sys.stderr.write(err_msg)
        sys.stderr.flush()
        with open("oauth_debug.log", "a") as f:
            f.write(err_msg)
        return super().on_authentication_error(request, provider, error=error, exception=exception, extra_context=extra_context)

    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return
        
        email = sociallogin.account.extra_data.get('email')
        if not email:
            return

        from users.models import CustomUser
        from allauth.socialaccount.models import SocialAccount
        try:
            user = CustomUser.objects.get(email=email)
            if not user.is_active:
                user.is_active = True
                user.save()

            if not SocialAccount.objects.filter(user=user, provider=sociallogin.account.provider).exists():
                sociallogin.account.user = user
                sociallogin.account.save()
            sociallogin.user = user
            
            if user.role == 'STUDENT' and not hasattr(user, 'student_profile'):
                code = generate_memorable_student_code(user.first_name, user.last_name)
                Student.objects.create(
                    user=user,
                    student_code=code,
                    school_name='',
                    parent_name='',
                    parent_phone='',
                    status='ACTIVE'
                )
        except CustomUser.DoesNotExist:
            pass

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user.is_active = True
        if not user.role:
            user.role = 'STUDENT'
        user.save()

        if user.role == 'STUDENT' and not hasattr(user, 'student_profile'):
            code = generate_memorable_student_code(user.first_name, user.last_name)
            Student.objects.create(
                user=user,
                student_code=code,
                school_name='',
                parent_name='',
                parent_phone='',
                status='ACTIVE'
            )
        return user

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        if not user.first_name and data.get('first_name'):
            user.first_name = data.get('first_name')
        if not user.last_name and data.get('last_name'):
            user.last_name = data.get('last_name')
        return user
