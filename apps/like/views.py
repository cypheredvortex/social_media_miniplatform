from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Like
from apps.post.models import Post


@login_required
@require_POST
def like_post(request, post_id):
    """
    Toggle like on a post.
    If user already liked → unlike.
    If not → create like.
    """

    post = get_object_or_404(Post, id=post_id)
    user = request.user

    # Check if like exists
    existing_like = Like.objects.filter(user=user, post=post).first()

    if existing_like:
        # Unlike
        existing_like.delete()
        return JsonResponse({
            "status": "unliked",
            "likes_count": Like.objects.filter(post=post).count()
        })

    else:
        # Create Like
        Like.objects.create(user=user, post=post)

        return JsonResponse({
            "status": "liked",
            "likes_count": Like.objects.filter(post=post).count()
        })
