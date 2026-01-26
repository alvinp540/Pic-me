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
