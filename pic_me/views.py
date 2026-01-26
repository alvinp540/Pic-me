from django.shortcuts import render

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
