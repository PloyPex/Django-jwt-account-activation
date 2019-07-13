from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
	UserCreationForm, PasswordResetForm)

User = get_user_model()

class UserAdminCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required
	fields, plus a repeated password."""
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'email')

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(UserAdminCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user


class UserAdminChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ('username', 'email', 'password', 'is_active', 'is_staff')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]
