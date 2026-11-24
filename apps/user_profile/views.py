from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render

from apps.audits.models import Audit


@login_required
def profile_view(request):
    user = request.user

    # Only this user's audits, with counts fetched in the same query
    user_audits = (
        Audit.objects
        .filter(submitted_by_user=user)
        .select_related('establishment')
        .annotate(
            verification_total=Count('verifications', distinct=True),
            photo_total=Count('photos', distinct=True),
        )
        .order_by('-created_at')
    )

    context = {
        'profile': getattr(user, 'profile', None),
        'user_audits': user_audits,
        'audit_count': user_audits.count(),
    }
    return render(request, 'user_profile/profile.html', context)