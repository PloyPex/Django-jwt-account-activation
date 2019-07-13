import jwt

from django.dispatch import receiver
from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models.signals import pre_save, post_save
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes

from datetime import datetime, timedelta

from .tokens import account_activation_token

User = get_user_model()

@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, *args, **kwargs):
	if created:
		data = {
			# 'uidb64': urlsafe_base64_encode(force_bytes(instance.pk)).decode(),
			'uidb64': urlsafe_base64_encode(force_bytes(instance.pk)),
			'token': account_activation_token.make_token(instance),
			'exp': datetime.utcnow() + timedelta(days=2),
			'iss': 'PloyPex:Accounts',
			'aud': 'PloyPex:Users',
			'iat': datetime.utcnow()
		}
		key = jwt.encode(data, settings.SECRET_KEY, algorithm='HS256').decode()
		message = render_to_string('registration/emails/account_activation_email.html', {
			'key': key
		})

		# you can also use 'email_user' method from custom User model
		email = EmailMessage(
			'Verify your email address',
			message,
			'PloyPex <noreply@ploypex.com>',
			[instance.email],
			reply_to=['support@ploypex.com']
		)
		email.content_subtype = "html"  # Main content is now text/html
		email.send()
