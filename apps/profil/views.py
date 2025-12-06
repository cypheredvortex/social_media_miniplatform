from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import Http404
from .models import Profile


def admin_profile_list(request):
    # Fetch all profiles with their related users
    profiles = Profile.objects.select_related('user').all().order_by('-id')
    return render(request, 'admin/admin_profile_list.html', {'profiles': profiles})



# --- View profile details ---
def admin_profile_detail(request, profile_id):
    try:
        profile_id = int(profile_id)
    except (ValueError, TypeError):
        raise Http404("Invalid profile ID")

    profile = get_object_or_404(Profile.objects.select_related('user'), id=profile_id)
    return render(request, 'admin/admin_profile_detail.html', {'profile': profile})


# --- Edit a profile ---
def admin_profile_edit(request, profile_id):
    try:
        profile_id = int(profile_id)
    except (ValueError, TypeError):
        raise Http404("Invalid profile ID")

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
        return redirect('profil:admin_profile_detail', profile_id=profile.id)

    return render(request, 'admin/admin_profile_edit.html', {'profile': profile})
