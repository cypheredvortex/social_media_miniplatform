import os
import django
import random
from faker import Faker
import sys

# --- Setup Django environment ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_miniplatform.settings")
django.setup()

from apps.user.models import User
from apps.profil.models import Profile

fake = Faker()

def seed_profiles():
    print("Deleting existing profiles...")
    Profile.objects.all().delete()
    print("Existing profiles deleted.")

    users = User.objects.all()
    if not users:
        print("No users found. Seed some users first.")
        return

    print(f"Seeding profiles for {users.count()} users...")
    for user in users:
        profile = Profile.objects.create(
            user=user,
            bio=fake.paragraph(nb_sentences=3),
            location=fake.city(),
            avatar_url=fake.image_url(),
            birthdate=fake.date_of_birth(minimum_age=18, maximum_age=70),
            website=fake.url()
        )
        print(f"Created profile for user: {user.username}")

    print("Seeding complete.")

if __name__ == "__main__":
    seed_profiles()
