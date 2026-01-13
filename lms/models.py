from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("dosen", "Dosen"),
        ("mahasiswa", "Mahasiswa"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="mahasiswa")

    def __str__(self):
        return f"{self.username} ({self.role})"


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
