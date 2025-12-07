# apps/like/views.py
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Like
# FIX: Import from content.models, not post.models
from apps.content.models import Content  # Changed this line

@login_required
@require_POST
def like_post(request, post_id):
    """
    Toggle like on a post.
    If user already liked → unlike.
    If not → create like.
    """
    # FIX: Get Content object instead of Post
    content = get_object_or_404(Content, id=post_id)
    
    # Ensure it's a POST, not a comment
    if content.content_type != 'POST':
        return JsonResponse({
            "status": "error",
            "message": "Can only like posts"
        }, status=400)
    
    user = request.user

    # Check if like exists
    existing_like = Like.objects.filter(user=user, content=content).first()

    if existing_like:
        # Unlike
        existing_like.delete()
        return JsonResponse({
            "status": "unliked",
            "likes_count": Like.objects.filter(content=content).count()
        })

    else:
        # Create Like
        Like.objects.create(user=user, content=content)

        return JsonResponse({
            "status": "liked",
            "likes_count": Like.objects.filter(content=content).count()
        })