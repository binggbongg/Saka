from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Establishment, Audit, AuditPhoto, AuditVerification

# Temporary preset establishments for testing prior to Google Maps integration
SAMPLE_ESTABLISHMENTS = [
    {
        "name": "CIT-U Main Campus (Library & Admin)",
        "category": "Education",
        "address_text": "N. Bacalso Ave, Cebu City",
        "latitude": 10.297400,
        "longitude": 123.878400,
    },
    {
        "name": "Ayala Center Cebu",
        "category": "Mall / Commercial",
        "address_text": "Cebu Business Park, Cebu City",
        "latitude": 10.317300,
        "longitude": 123.905800,
    },
    {
        "name": "Fuente Osmeña Circle Public Park",
        "category": "Public Space",
        "address_text": "Osmeña Blvd, Cebu City",
        "latitude": 10.311400,
        "longitude": 123.892600,
    },
    {
        "name": "Chong Hua Hospital Fuente",
        "category": "Healthcare",
        "address_text": "Fuente Osmeña, Cebu City",
        "latitude": 10.312900,
        "longitude": 123.891700,
    },
]


def audit_list_view(request):
    """Displays all submitted audits and registered establishments."""
    audits = Audit.objects.select_related('establishment', 'submitted_by_user').all().order_by('-created_at')
    establishments = Establishment.objects.all().order_by('name')
    return render(request, 'audits/audit_list.html', {
        'audits': audits,
        'establishments': establishments
    })


def audit_detail_view(request, audit_id):
    """Displays specific accessibility details, photos, and verifications for an audit."""
    audit = get_object_or_404(
        Audit.objects.select_related('establishment', 'submitted_by_user'), 
        audit_id=audit_id
    )
    photos = audit.photos.all()
    verifications = audit.verifications.select_related('user').all()
    
    return render(request, 'audits/audit_detail.html', {
        'audit': audit,
        'photos': photos,
        'verifications': verifications
    })


@login_required
def create_audit_view(request):
    """Allows an authenticated user to submit an accessibility audit."""
    # Seed mock establishments if the database has none yet
    if not Establishment.objects.exists():
        for item in SAMPLE_ESTABLISHMENTS:
            Establishment.objects.get_or_create(
                name=item["name"],
                defaults={
                    "category": item["category"],
                    "address_text": item["address_text"],
                    "latitude": item["latitude"],
                    "longitude": item["longitude"],
                    "added_by_user": request.user,
                }
            )

    if request.method == 'POST':
        establishment_id = request.POST.get('establishment_id')
        establishment = get_object_or_404(Establishment, establishment_id=establishment_id)

        # Checkboxes return 'on' if checked, None if unchecked
        new_audit = Audit.objects.create(
            establishment=establishment,
            submitted_by_user=request.user,
            has_ramp_step_free=bool(request.POST.get('has_ramp_step_free')),
            has_wide_door=bool(request.POST.get('has_wide_door')),
            has_elevator=bool(request.POST.get('has_elevator')),
            has_accessible_restroom=bool(request.POST.get('has_accessible_restroom')),
            has_tactical_signage=bool(request.POST.get('has_tactical_signage')),
            status=False
        )

        # Optional photo link upload
        photo_url = request.POST.get('image_url', '').strip()
        if photo_url:
            AuditPhoto.objects.create(
                audit=new_audit,
                image_url=photo_url
            )

        return redirect('audit_detail', audit_id=new_audit.audit_id)

    establishments = Establishment.objects.all().order_by('name')
    return render(request, 'audits/create_audit.html', {'establishments': establishments})


@login_required
def verify_audit_view(request, audit_id):
    """Records an upvote, confirmation, or review action from another user."""
    audit = get_object_or_404(Audit, audit_id=audit_id)
    if request.method == 'POST':
        action_type = request.POST.get('action', 'verified')
        AuditVerification.objects.create(
            audit=audit,
            user=request.user,
            action=action_type
        )
    return redirect('audit_detail', audit_id=audit.audit_id)