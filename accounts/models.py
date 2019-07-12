from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser
)
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.core.mail import send_mail

from django.conf import settings

from .validators import temp_email_validator
from .managers import UserManager

class User(AbstractBaseUser):
	username_validator = UnicodeUsernameValidator()

	username = models.CharField(
		_('username'),
		max_length=150,
		unique=True,
		help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
		validators=[username_validator],
		error_messages={
			'unique': _("A user with that username already exists."),
		},
	)

	email = models.EmailField(
		_('email address'),
		unique=True,
		max_length=255,
		validators=[validate_email, temp_email_validator],
		error_messages={
			'unique': _("A user with that email address already exists."),
		},
	)
	is_staff = models.BooleanField(
		_('staff status'),
		default=False,
		help_text=_('Designates whether the user can log into this admin site.'),
	)
	is_active = models.BooleanField(
		_('active'),
		default=True,
		help_text=_(
			'Designates whether this user should be treated as active. '
			'Unselect this instead of deleting accounts.'
		),
	)
	is_superuser = models.BooleanField(
		_('superuser status'),
		default=False,
		help_text=_(
			'Designates that this user has all permissions without '
			'explicitly assigning them.'
		),
	)
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

	objects = UserManager()

	EMAIL_FIELD = 'email'
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')

	def clean(self):
		super().clean()
		self.email = self.__class__.objects.normalize_email(self.email)

	def get_full_name(self):
		"""
		Return the first_name plus the last_name, with a space in between.
		"""
		return str(self.email)

	def get_short_name(self):
		"""Return the short name for the user."""
		return self.username

	# def get_email_field_name(self):
	# 	"""Return the email of the user"""
	# 	return str(self.email)

	@classmethod
	def get_email_field_name(cls):
		try:
			return cls.EMAIL_FIELD
		except AttributeError:
			return 'email'

	def email_user(self, subject, message, from_email=None, **kwargs):
		"""Send an email to this user."""
		send_mail(subject, message, from_email, [self.email], **kwargs)

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True
