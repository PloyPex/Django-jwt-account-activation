from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.db.models.signals import pre_save, post_save
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

User = get_user_model()

@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, *args, **kwargs):
	if created:
		message = render_to_string('registration/emails/account_activation_email.html', {
			'user': user,
			'domain': domain,
			# 'uidb64': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
			'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
			'token': account_activation_token.make_token(user)
		})

		# you can also use 'email_user' method from custom User model
		email = EmailMessage(
			'Verify your email address',
			message,
			'PloyPex <noreply@ploypex.com>',
			[instance.email],
			reply_to=['support@ploypex.com']
		)
		msg.content_subtype = "html"  # Main content is now text/html
		msg.send()
