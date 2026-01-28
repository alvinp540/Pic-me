

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import UserProfile, Photo

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """
    Extended user registration form with email field.
    Automatically creates a UserProfile via post_save signal.
    """
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomUserForm(forms.ModelForm):
    """
    Form for updating CustomUser information (username, first_name, last_name, email).
    Follows the guide pattern for basic user information updates.
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information (bio and profile picture).
    """
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'profile_picture': forms.FileInput(attrs={'onchange': 'previewProfilePicture(event)'}),
        }


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating basic user information.
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class PhotoUploadForm(forms.ModelForm):
    """
    Form for uploading new photos to the gallery.
    """
    class Meta:
        model = Photo
        fields = ['title', 'description', 'image', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'tags': forms.CheckboxSelectMultiple(),
        }