from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required
from bson import ObjectId

from .models import Profile
from apps.user.models import User
from apps.content.models import Content
from apps.follow.models import Follow

# ---------------------------
# Admin Profile Views
# ---------------------------

def admin_profile_list(request):
    # Fetch all profiles with their related users
    profiles = Profile.objects.select_related('user').all().order_by('-id')
    return render(request, 'admin/admin_profile_list.html', {'profiles': profiles})

def admin_profile_detail(request, profile_id):
    # Get profile by ID (NOT username)
    profile = get_object_or_404(Profile.objects.select_related('user'), id=ObjectId(profile_id))
    
    # Get user's posts count
    post_count = Content.objects.filter(author=profile.user, content_type='POST').count()
    
    # Get follower/following counts
    followers_count = Follow.objects.filter(followed=profile.user).count()
    following_count = Follow.objects.filter(follower=profile.user).count()
    
    context = {
        'profile': profile,
        'user': profile.user,
        'post_count': post_count,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    
    return render(request, 'admin/admin_profile_detail.html', context)

def admin_profile_edit(request, profile_id):
    profile = get_object_or_404(Profile.objects.select_related('user'), id=ObjectId(profile_id))

    if request.method == "POST":
        bio = request.POST.get("bio", "").strip()
        location = request.POST.get("location", "").strip()
        avatar_url = request.POST.get("avatar_url", "").strip()
        birthdate = request.POST.get("birthdate", "").strip()
        website = request.POST.get("website", "").strip()

        profile.update_info(
            bio=bio or None,
            location=location or None,
            avatar_url=avatar_url or None,
            birthdate=birthdate or None,
            website=website or None
        )

        messages.success(request, f"Profile for {profile.user.username} updated successfully.")
        return redirect("profil:admin_profile_detail", profile_id=profile_id)

    return render(request, "admin/admin_profile_edit.html", {"profile": profile})

# ---------------------------
# Regular User Profile Views
# ---------------------------

@login_required
def my_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Get user's posts
    posts = Content.objects.filter(
        author=request.user,
        content_type='POST',
        status='ACTIVE'
    ).order_by('-created_at')
    
    # Get counts
    post_count = Content.objects.filter(author=request.user, content_type='POST').count()
    followers_count = Follow.objects.filter(followed=request.user).count()
    following_count = Follow.objects.filter(follower=request.user).count()
    
    context = {
        'profile': profile,
        'user': request.user,
        'posts': posts,
        'post_count': post_count,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_own_profile': True,
    }
    
    return render(request, 'profil/my_profile.html', context)

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        bio = request.POST.get("bio", "").strip()
        location = request.POST.get("location", "").strip()
        avatar_url = request.POST.get("avatar_url", "").strip()
        birthdate = request.POST.get("birthdate", "").strip()
        website = request.POST.get("website", "").strip()
        
        profile.update_info(
            bio=bio or None,
            location=location or None,
            avatar_url=avatar_url or None,
            birthdate=birthdate or None,
            website=website or None
        )
        
        messages.success(request, "Profile updated successfully.")
        return redirect("profil:my_profile")
    
    return render(request, "profil/edit_profile.html", {"profile": profile})

@login_required
def view_profile(request, user_id):
    user = get_object_or_404(User, id=ObjectId(user_id))
    profile, created = Profile.objects.get_or_create(user=user)
    
    # Check if current user is following this user
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            followed=user
        ).exists()
    
    # Get user's public posts
    posts = Content.objects.filter(
        author=user,
        content_type='POST',
        status='ACTIVE',
        visibility='PUBLIC'
    ).order_by('-created_at')
    
    # Get counts
    post_count = Content.objects.filter(author=user, content_type='POST').count()
    followers_count = Follow.objects.filter(followed=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    
    context = {
        'profile': profile,
        'user': user,
        'posts': posts,
        'post_count': post_count,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_own_profile': request.user == user,
        'is_following': is_following,
    }
    
    return render(request, 'profil/view_profile.html', context)