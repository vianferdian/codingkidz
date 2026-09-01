from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager 
from django.core.validators import RegexValidator
from django.contrib.auth.models import Group




class CustomAccountManager(BaseUserManager):

	def create_superuser(self, email, first_name, last_name, password,**other_fields):
		other_fields.setdefault('is_staff',True)
		other_fields.setdefault('is_superuser',True)
		other_fields.setdefault('is_active',True)
		other_fields.setdefault('role','ADMIN')

		if other_fields.get('is_staff') is not True:
			raise ValueError(
				'Superuser must be assigned to is_staff=True.')
		if other_fields.get('is_superuser') is not True:
			raise ValueError(
				'Superuser must be assigned to is_superuser=True.')


		super_user = self.create_user(email,first_name, last_name, password, **other_fields)

		return super_user


	def create_user(self, email, first_name, last_name, password,**other_fields):
		# email validation
		if not email:
			raise ValueError(_('You must provide an email address'))

		email = self.normalize_email(email)
		user = self.model(email=email, first_name=first_name, last_name=last_name, **other_fields)
		user.set_password(password)
		user.save()
		return user


def user_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	return f'{instance.email}/{filename}'

#This is the new custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin):
	GENDER_CHOICES = (
		('','Choose gender'),
		('Male', 'Male'),
		('Female', 'Female'),
		('Others', 'Others'),
	)

	ROLE_CHOICES = (
		('ADMIN', 'Admin'),
		('TUTOR', 'Tutor'),
		('GURU', 'Guru'),
		('STUDENT', 'Student'),
	)
	STATUS_CHOICES = (
		('ACTIVE', 'Active'),
		('INACTIVE', 'Inactive'),
		('PENDING', 'Pending'),
	)

	email = models.EmailField(_('email address'),unique=True)
	first_name = models.CharField(max_length=150,blank=True)
	last_name = models.CharField(max_length=150,blank=True)
	gender = models.CharField(max_length=100, choices=GENDER_CHOICES,blank=True)
	avatar = models.ImageField(upload_to=user_directory_path, default="profile/image/default.gif")
	dob = models.CharField(max_length=150,blank=True,null=True,help_text="Pattern = dd-mm-yyyy")
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)# Validators should be a list
	groups = models.ManyToManyField(Group,blank=True)
	about = models.TextField(_('about'),max_length=500,blank=True)
	role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)# this false work on ui not in admin
	#when user is created, than system send a email after varify  user is active

	objects = CustomAccountManager()

	USERNAME_FIELD = 'email'  
	REQUIRED_FIELDS = ['first_name','last_name']

	def __str__(self):
		return f"{self.first_name} {self.last_name} ({self.role})"


class ActivityLog(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
	action = models.CharField(max_length=255)
	model = models.CharField(max_length=100, blank=True, null=True)
	object_id = models.PositiveIntegerField(blank=True, null=True)
	description = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user} - {self.action} on {self.model} at {self.created_at}"