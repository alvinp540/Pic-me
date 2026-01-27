from typing import Optional
from django.contrib.auth import get_user_model


class EmailAuthBackend:
    """Authenticate using an email address and password.

    This backend supports authenticating with the email field 
    while still allowing Django's ModelBackend to
    handle permission checks when needed.
    """

    def authenticate(self, request, username: Optional[str] = None, password: Optional[str] = None, **kwargs):
        UserModel = get_user_model()
        email = username or kwargs.get('email')
        if email is None or password is None:
            return None
        try:
            user = UserModel.objects.get(email__iexact=email)
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

    def user_can_authenticate(self, user):
        return getattr(user, 'is_active', True)
