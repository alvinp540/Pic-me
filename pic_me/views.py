from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Photo, Tag, PhotoInteraction, UserProfile
from .forms import UserRegistrationForm, UserProfileForm, UserUpdateForm, PhotoUploadForm


# Create your views here.

def home(request):
    """
    Display the photo gallery homepage with optional tag filtering.
    """
    photos = Photo.objects.all().prefetch_related('tags', 'interactions')
    tags = Tag.objects.all()
    
    tag_filter = request.GET.get('tag')
    if tag_filter:
        photos = photos.filter(tags__slug=tag_filter)
    
    search_query = request.GET.get('search')
    if search_query:
        photos = photos.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    context = {
        'photos': photos,
        'tags': tags,
        'selected_tag': tag_filter,
        'search_query': search_query,
    }
    return render(request, 'pic_me/home.html', context)


def photo_detail(request, photo_id):
    """
    Display detailed information for a specific photo.
    """
    photo = get_object_or_404(Photo, id=photo_id)
    user_interaction = None
    
    if request.user.is_authenticated:
        user_interaction = PhotoInteraction.objects.filter(
            user=request.user, 
            photo=photo
        ).first()
    
    context = {
        'photo': photo,
        'user_interaction': user_interaction,
        'total_likes': photo.total_likes(),
        'total_dislikes': photo.total_dislikes(),
    }
    return render(request, 'pic_me/photo_detail.html', context)

def register(request):
    """
    Handle user registration with form validation.
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created successfully for {user.username}!')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'pic_me/register.html', {'form': form})


def user_login(request):
    """
    Handle user login with authentication.
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'pic_me/login.html')


def user_logout(request):
    """
    Handle user logout.
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile(request):
    """
    Display and update user profile information.
    """
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'pic_me/profile.html', context)


@login_required
def interact_photo(request, photo_id):
    """
    Handle user interactions with photos.
    """
    if request.method == 'POST':
        photo = get_object_or_404(Photo, id=photo_id)
        interaction_type = request.POST.get('interaction_type')
        
        if interaction_type not in ['like', 'dislike']:
            messages.error(request, 'Invalid interaction type.')
            return redirect('photo_detail', photo_id=photo_id)
        
        interaction, created = PhotoInteraction.objects.get_or_create(
            user=request.user,
            photo=photo,
            defaults={'interaction_type': interaction_type}
        )
        
        if not created:
            if interaction.interaction_type == interaction_type:
                interaction.delete()
                messages.info(request, f'{interaction_type.capitalize()} removed.')
            else:
                interaction.interaction_type = interaction_type
                interaction.save()
                messages.success(request, f'Changed to {interaction_type}.')
        else:
            messages.success(request, f'Photo {interaction_type}d!')
        
        return redirect('photo_detail', photo_id=photo_id)
    
    return redirect('home')

