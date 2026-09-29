from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Establishment(models.Model):
    establishment_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=50)
    address_text = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    aggregate_tagging = models.CharField(max_length=255, blank=True, null=True)
    
    # Foreign key added_by_user_id -> User
    added_by_user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='added_establishments',
        db_column='added_by_user_id'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Audit(models.Model):
    audit_id = models.AutoField(primary_key=True)
    
    # Foreign key establishment_id -> Establishment
    establishment = models.ForeignKey(
        Establishment, 
        on_delete=models.CASCADE, 
        related_name='audits',
        db_column='establishment_id'
    )
    
    # Foreign key submitted_by_user_id -> User
    submitted_by_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='submitted_audits',
        db_column='submitted_by_user_id'
    )
    
    # Accessibility feature booleans
    has_ramp_step_free = models.BooleanField(default=False)
    has_wide_door = models.BooleanField(default=False)
    has_elevator = models.BooleanField(default=False)
    has_accessible_restroom = models.BooleanField(default=False)
    has_tactical_signage = models.BooleanField(default=False)
    
    status = models.BooleanField(default=False)  # or CharField if using statuses like 'pending'/'verified'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audit #{self.audit_id} - {self.establishment.name}"

class AuditPhoto(models.Model):
    photo_id = models.AutoField(primary_key=True)
    
    # Foreign key audit_id -> Audit
    audit = models.ForeignKey(
        Audit, 
        on_delete=models.CASCADE, 
        related_name='photos',
        db_column='audit_id'
    )
    image_url = models.URLField(max_length=500)  # Or models.ImageField(upload_to='audit_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo #{self.photo_id} for Audit #{self.audit_id}"

class AuditVerification(models.Model):
    id = models.AutoField(primary_key=True)
    
    # Foreign key audit_id -> Audit
    audit = models.ForeignKey(
        Audit, 
        on_delete=models.CASCADE, 
        related_name='verifications',
        db_column='audit_id'
    )
    
    # Foreign key user_id -> User
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='audit_verifications',
        db_column='user_id'
    )
    
    action = models.CharField(max_length=50)  # e.g., 'upvote', 'downvote', 'verify'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verification by {self.user.username} on Audit #{self.audit_id}"