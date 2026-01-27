from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import UserProfile, Photo, Tag, PhotoInteraction

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
	list_display = ('email', 'username', 'is_staff', 'is_active')
	search_fields = ('email', 'username')


admin.site.register(UserProfile)
admin.site.register(Photo)
admin.site.register(Tag)
admin.site.register(PhotoInteraction)
