from django.conf import settings
from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
import os


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name or self.username

class UserProfile(models.Model):
    """
    Extended user profile model containing additional user information.
    Linked to the CustomUser model via OneToOne relationship.
    Automatically created when a new user is created via post_save signal.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, help_text="Tell us about yourself")
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


# Signal handlers for automatic profile creation and saving
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a UserProfile when a new CustomUser is created.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the UserProfile when the CustomUser is saved.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()


class Tag(models.Model):
    """
    Tag model for categorizing photos.
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        


class Photo(models.Model):
    """
    Photo model representing individual photos in the gallery.
    Includes title, description, tags, and tracks user interactions.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='photos/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])]
    )
    tags = models.ManyToManyField(Tag, related_name='photos', blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        """Calculate total number of likes for this photo."""
        return self.interactions.filter(interaction_type='like').count()

    def total_dislikes(self):
        """Calculate total number of dislikes for this photo."""
        return self.interactions.filter(interaction_type='dislike').count()

    @staticmethod
    def create_placeholder_image(width=400, height=300, color=(100, 150, 200), text=""):
        """
        Create a placeholder image programmatically.
        Returns a PIL Image object.
        
        Args:
            width: Image width in pixels (default 400)
            height: Image height in pixels (default 300)
            color: RGB tuple for background color (default light blue)
            text: Text to display on the image (default empty)
        
        Returns:
            PIL Image object
        """
        image = Image.new('RGB', (width, height), color=color)
        return image

    @staticmethod
    def create_solid_image(width=400, height=300, color=(100, 150, 200)):
        """
        Create a solid color image.
        Returns the image as a ContentFile suitable for ImageField.
        """
        image = Photo.create_placeholder_image(width, height, color)
        
        # Convert to bytes
        image_bytes = BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes.seek(0)
        
        return ContentFile(image_bytes.getvalue(), name='placeholder.png')

    @classmethod
    def create_with_placeholder(cls, title, description, uploaded_by, color=(100, 150, 200), tags=None):
        """
        Create a Photo with a generated placeholder image.
        
        Args:
            title: Photo title
            description: Photo description
            uploaded_by: User object who uploaded the photo
            color: RGB tuple for background color
            tags: List of Tag objects to associate with photo
            
        Returns:
            Photo object
        """
        photo = cls.objects.create(
            title=title,
            description=description,
            uploaded_by=uploaded_by,
            image=cls.create_solid_image(color=color)
        )
        
        if tags:
            photo.tags.set(tags)
        
        return photo

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

class PhotoInteraction(models.Model):
    """
    Model to track user interactions with photos.
    Ensures a user can only have one interaction per photo.
    """
    INTERACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interactions')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'photo')
        verbose_name = 'Photo Interaction'
        verbose_name_plural = 'Photo Interactions'

    def __str__(self):
        verb = 'liked' if self.interaction_type == 'like' else 'disliked'
        return f"{self.user.username} {verb} {self.photo.title}"