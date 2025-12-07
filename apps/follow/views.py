from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from bson import ObjectId
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Follow
from apps.user.models import User

@login_required
@require_POST
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=ObjectId(user_id))
    
    if user_to_follow == request.user:
        return JsonResponse({
            'error': 'You cannot follow yourself'
        }, status=400)
    
    # Check if already following
    existing_follow = Follow.objects.filter(
        follower=request.user,
        followed=user_to_follow
    ).first()
    
    if existing_follow:
        return JsonResponse({
            'error': 'Already following this user'
        }, status=400)
    
    # Create follow relationship
    Follow.objects.create(
        follower=request.user,
        followed=user_to_follow
    )
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'You are now following {user_to_follow.username}'
        })
    
    messages.success(request, f'You are now following {user_to_follow.username}')
    return redirect('profil:view', user_id=user_id)

@login_required
@require_POST
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=ObjectId(user_id))
    
    follow = Follow.objects.filter(
        follower=request.user,
        followed=user_to_unfollow
    ).first()
    
    if follow:
        follow.delete()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'You have unfollowed {user_to_unfollow.username}'
        })
    
    messages.success(request, f'You have unfollowed {user_to_unfollow.username}')
    return redirect('profil:view', user_id=user_id)

@login_required
def followers_list(request):
    followers = Follow.objects.filter(followed=request.user).select_related('follower')
    return render(request, 'follow/followers.html', {'followers': followers})

@login_required
def following_list(request):
    following = Follow.objects.filter(follower=request.user).select_related('followed')
    return render(request, 'follow/following.html', {'following': following})