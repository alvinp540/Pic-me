from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class CustomAuthBackend(BaseBackend):
    """
    Custom authentication backend that authenticates users by email and password.
    Validates email and password against the CustomUser model.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Authenticate a user by email and password.
        Returns the user object if authentication is successful, None otherwise.
        """
        UserModel = get_user_model()
        
        if email is None or password is None:
            return None
        
        try:
            user = UserModel.objects.get(email=email)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except UserModel.DoesNotExist:
            return None
        
        return None

    def get_user(self, user_id):
        """
        Retrieve a user object by user ID.
        Returns the user object if found, None otherwise.
        """
        UserModel = get_user_model()
        
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

    def user_can_authenticate(self, user):
        """
        Check if the user account is active.
        """
        return getattr(user, 'is_active', True)
