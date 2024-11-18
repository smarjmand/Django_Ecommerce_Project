from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User


class UserVerificationTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        user_id = six.text_type(user.pk)
        ts = six.text_type(timestamp)
        is_active = six.text_type(user.is_active)
        return f"{user_id}{ts}{is_active}"


user_token_generator = UserVerificationTokenGenerator()


def send_verification_email(user: User, domain):
    subject = 'سفارش چی | فعال سازی حساب کاربری'
    message = render_to_string(
        'account/email/verification_email.html',
        {
            'user': user,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': user_token_generator.make_token(user=user)
        }
    )
    user.email_user(subject=subject, message=message)