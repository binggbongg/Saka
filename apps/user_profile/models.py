from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    MOBILITY_CHOICES = [
        ('none', 'None'),
        ('manual_wheelchair', 'Manual Wheelchair'),
        ('power_wheelchair', 'Power / Electric Wheelchair'),
        ('cane', 'Cane / Walking Stick'),
        ('crutches', 'Crutches'),
        ('walker', 'Walker / Rollator'),
        ('guide_dog', 'Guide Dog / Service Animal'),
        ('other', 'Other'),
    ]

    mobility_aid_type = models.CharField(
        max_length=50,
        choices=MOBILITY_CHOICES,
        default='none',
        blank=True,
        null=True
    )

    full_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(max_length=300, blank=True)
    profile_image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username