from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from lms.models import Course


class Command(BaseCommand):
    help = "Seed initial users and courses"

    def handle(self, *args, **options):
        User = get_user_model()

        user_payloads = [
            {
                "username": "superadmin",
                "email": "superadmin@example.com",
                "password": "password123",
                "role": "admin",
                "is_staff": True,
                "is_superuser": True,
            },
            {
                "username": "dosen",
                "email": "dosen@example.com",
                "password": "password123",
                "role": "dosen",
                "is_staff": True,
                "is_superuser": False,
            },
            {
                "username": "mahasiswa",
                "email": "mahasiswa@example.com",
                "password": "password123",
                "role": "mahasiswa",
                "is_staff": False,
                "is_superuser": False,
            },
        ]

        for payload in user_payloads:
            user, created = User.objects.get_or_create(
                username=payload["username"],
                defaults={
                    "email": payload["email"],
                    "role": payload["role"],
                    "is_staff": payload["is_staff"],
                    "is_superuser": payload["is_superuser"],
                },
            )
            if created:
                user.set_password(payload["password"])
                user.save()
                self.stdout.write(f"Created user {user.username}")
            else:
                # Keep seed data deterministic
                user.email = payload["email"]
                user.role = payload["role"]
                user.is_staff = payload["is_staff"]
                user.is_superuser = payload["is_superuser"]
                if not user.check_password(payload["password"]):
                    user.set_password(payload["password"])
                user.save()
                self.stdout.write(f"Updated user {user.username}")

        courses = [
            {
                "title": "Pengantar Pemrograman",
                "description": "Dasar-dasar pemrograman dan logika algoritma.",
            },
            {
                "title": "Basis Data Lanjutan",
                "description": "Perancangan basis data relasional dan optimasi kueri.",
            },
            {
                "title": "Jaringan Komputer",
                "description": "Konsep jaringan, protokol, dan keamanan dasar.",
            },
            {
                "title": "Pengembangan Web",
                "description": "Membangun aplikasi web dengan backend dan frontend dasar.",
            },
            {
                "title": "Kecerdasan Buatan",
                "description": "Pengenalan AI, machine learning, dan aplikasinya.",
            },
        ]

        for course in courses:
            course_obj, created = Course.objects.get_or_create(
                title=course["title"], defaults={"description": course["description"]}
            )
            action = "Created" if created else "Skipped"
            self.stdout.write(f"{action} course {course_obj.title}")

        self.stdout.write(self.style.SUCCESS("Seeding complete."))
