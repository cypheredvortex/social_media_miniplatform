import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_miniplatform.settings")
django.setup()

from django.urls import reverse, NoReverseMatch
from apps.user.models import User
from apps.content.models import Content
from apps.profil.models import Profile
from apps.report.models import Report

print("Testing URL patterns...")
print("="*60)

# Test with actual data
try:
    # Get first user
    user = User.objects.first()
    if user:
        print(f"Testing user URLs for: {user.username}")
        print(f"  User ID: {user.id}")
        print(f"  Type: {type(user.id)}")
        
        # Test user admin URLs
        try:
            url = reverse('user:admin_user_detail', args=[user.id])
            print(f"  ✓ admin_user_detail URL: {url}")
        except NoReverseMatch as e:
            print(f"  ✗ Error with admin_user_detail: {e}")
        
        try:
            url = reverse('user:admin_user_suspend', args=[user.id])
            print(f"  ✓ admin_user_suspend URL: {url}")
        except NoReverseMatch as e:
            print(f"  ✗ Error with admin_user_suspend: {e}")
    
    # Get first content
    content = Content.objects.first()
    if content:
        print(f"\nTesting content URLs for content: {content.id}")
        try:
            url = reverse('content:admin_content_detail', args=[content.id])
            print(f"  ✓ admin_content_detail URL: {url}")
        except NoReverseMatch as e:
            print(f"  ✗ Error with admin_content_detail: {e}")
    
    # Get first profile
    profile = Profile.objects.first()
    if profile:
        print(f"\nTesting profile URLs for profile: {profile.id}")
        try:
            url = reverse('profil:admin_profile_detail', args=[profile.id])
            print(f"  ✓ admin_profile_detail URL: {url}")
        except NoReverseMatch as e:
            print(f"  ✗ Error with admin_profile_detail: {e}")
    
    # Get first report
    report = Report.objects.first()
    if report:
        print(f"\nTesting report URLs for report: {report.id}")
        try:
            url = reverse('report:admin_report_detail', args=[report.id])
            print(f"  ✓ admin_report_detail URL: {url}")
        except NoReverseMatch as e:
            print(f"  ✗ Error with admin_report_detail: {e}")
    
    print("\n" + "="*60)
    print("URL Testing Complete")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()