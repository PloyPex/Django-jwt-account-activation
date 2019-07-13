import uuid

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.utils.crypto import salted_hmac
from django.utils.http import int_to_base36

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
	def _make_hash_value(self, user, timestamp):
		login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
		return (
			six.text_type(user.pk) + six.text_type(timestamp) +
			six.text_type(user.is_active) + six.text_type(user.employer_perm) +
			six.text_type(user.candidate_perm) + six.text_type(user.password) +
			six.text_type(login_timestamp)
		)

	def _make_token_with_timestamp(self, user, timestamp):
		# timestamp is number of days since 2001-1-1.  Converted to
		# base 36, this gives us a 3 digit string until about 2121
		ts_b36 = int_to_base36(timestamp)
		hash_string = salted_hmac(
			self.key_salt,
			self._make_hash_value(user, timestamp),
			secret=self.secret,
		).hexdigest()  # Limit to 20 characters to shorten the URL.
		return "%s-%s" % (ts_b36, hash_string)


account_activation_token = AccountActivationTokenGenerator()
