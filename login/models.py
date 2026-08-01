from django.db import models
from django.contrib.auth.models import User


# ---------------------------------------------------------
# USER PROFILE (roles)
# ---------------------------------------------------------

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("teacher", "Teacher"),
        ("student", "Student"),
        ("doctor", "Doctor"),
        ("nurse", "Nurse"),
        ("patient", "Patient"),
        ("user", "User"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# ---------------------------------------------------------
# NOTES
# ---------------------------------------------------------

class Note(models.Model):
    CATEGORY_CHOICES = [
        ("work", "Work"),
        ("personal", "Personal"),
        ("ideas", "Ideas"),
        ("urgent", "Urgent"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="other")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ---------------------------------------------------------
# TASKS
# ---------------------------------------------------------

class Task(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
