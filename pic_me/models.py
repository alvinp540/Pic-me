from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class UserProfile(models.Model):
    """
    Extended user profile model containing additional user information.
    Linked to Django's built-in User model via OneToOne relationship.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
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
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
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

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

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
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interactions') # User who interacted on deletion related interactions are deleted
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'photo')
        verbose_name = 'Photo Interaction'
        verbose_name_plural = 'Photo Interactions'

    def __str__(self):
        return f"{self.user.username} {self.interaction_type}d {self.photo.title}"