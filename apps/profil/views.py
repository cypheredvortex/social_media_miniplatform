from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import Http404
from .models import Profile
from bson import ObjectId


def admin_profile_list(request):
    # Fetch all profiles with their related users
    profiles = Profile.objects.select_related('user').all().order_by('-id')
    return render(request, 'admin/admin_profile_list.html', {'profiles': profiles})



# --- View profile details ---
def admin_profile_detail(request, profile_id):
    # Validate that profile_id is a valid ObjectId string
    try:
        obj_id = ObjectId(profile_id)
    except Exception:
        raise Http404("Invalid profile ID")

    # Fetch the profile and its related user
    profile = get_object_or_404(Profile.objects.select_related('user'), id=obj_id)

    # Render the template with a single profile
    return render(request, 'admin/admin_profile_detail.html', {'profile': profile})

# --- Edit a profile ---
def admin_profile_edit(request, profile_id):
    # DO NOT convert profile_id to int
    profile = get_object_or_404(Profile.objects.select_related('user'), id=profile_id)

    if request.method == 'POST':
        bio = request.POST.get('bio', '').strip()
        location = request.POST.get('location', '').strip()
        avatar_url = request.POST.get('avatar_url', '').strip()
        birthdate = request.POST.get('birthdate', '').strip() or None
        website = request.POST.get('website', '').strip()

        profile.update_info(
            bio=bio,
            location=location,
            avatar_url=avatar_url,
            birthdate=birthdate,
            website=website
        )

        messages.success(request, f'Profile of {profile.user.username} updated successfully.')
        return redirect('profil:admin_profile_detail', profile_id=str(profile.id))

    return render(request, 'admin/admin_profile_edit.html', {'profile': profile})
