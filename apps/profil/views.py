from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Profile
from bson import ObjectId
from django.http import Http404

# List all profiles
def admin_profile_list(request):
    # Profile model doesn't have a `created_at` field; order by id instead
    profiles = Profile.objects.all().order_by('-id')
    return render(request, 'admin/admin_profile_list.html', {'profiles': profiles})

# View profile details
def admin_profile_detail(request, profile_id):
    try:
        profile = get_object_or_404(Profile, id=ObjectId(profile_id))
    except:
        raise Http404("Profile does not exist")
    return render(request, 'admin/admin_profile_detail.html', {'profile': profile})


def admin_profile_edit(request, profile_id):
    try:
        profile = get_object_or_404(Profile, id=ObjectId(profile_id))
    except:
        raise Http404("Profile does not exist")

    if request.method == 'POST':
        profile.update_info(
            bio=request.POST.get('bio'),
            location=request.POST.get('location'),
            avatar_url=request.POST.get('avatar_url'),
            birthdate=request.POST.get('birthdate') or None,
            website=request.POST.get('website')
        )
        messages.success(request, f'Profile of {profile.user.username} updated successfully.')
        return redirect('profil:admin_profile_detail', profile_id=str(profile.id))

    return render(request, 'admin/admin_profile_edit.html', {'profile': profile})
