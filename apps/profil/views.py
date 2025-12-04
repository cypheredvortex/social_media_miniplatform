from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Profile

# List all profiles
def admin_profile_list(request):
    # Profile model doesn't have a `created_at` field; order by id instead
    profiles = Profile.objects.all().order_by('-id')
    return render(request, 'admin/admin_profile_list.html', {'profiles': profiles})

# View profile details
def admin_profile_detail(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    return render(request, 'admin/admin_profile_detail.html', {'profile': profile})

# Optional: edit profile info
def admin_profile_edit(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    if request.method == 'POST':
        profile.update_info(
            bio=request.POST.get('bio'),
            location=request.POST.get('location'),
            avatar_url=request.POST.get('avatar_url'),
            birthdate=request.POST.get('birthdate') or None,
            website=request.POST.get('website')
        )
        messages.success(request, f'Profile of {profile.user.username} updated successfully.')
        return redirect('profil:admin_profile_detail', profile_id=profile.id)
    return render(request, 'admin/admin_profile_edit.html', {'profile': profile})
