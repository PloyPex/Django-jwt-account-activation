from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode, is_safe_url
from django.views import View

from .tokens import account_activation_token

User = get_user_model()

class AccountActivate(View):
	def get(self, request, uidb64, token):
		try:
			uid = urlsafe_base64_decode(uidb64).decode()
			user = User.objects.get(pk=uid)
		except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
			print(e)
			user = None

		if user is not None and account_activation_token.check_token(user, token):
			user.is_active = True
			user.save()
			# login(request, user, backend='django.contrib.auth.backends.ModelBackend')
			# return redirect('login')
			return render(request, 'registration/account_activated.html')
		else:
			return render(request, 'registration/account_activation_invalid.html')
