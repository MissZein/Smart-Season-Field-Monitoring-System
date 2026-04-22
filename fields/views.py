from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Field

@login_required
def dashboard(request):
    user = request.user
    is_admin = user.groups.filter(name='Admins').exists() or user.is_superuser

    if is_admin:
        # Admins see everything [cite: 48]
        fields = Field.objects.all()
    else:
        # Agents only see their assigned fields [cite: 49]
        fields = Field.objects.filter(assigned_agent=user)

    # Simple summaries for the dashboard [cite: 50, 52]
    context = {
        'fields': fields,
        'total_fields': fields.count(),
        'at_risk_count': sum(1 for f in fields if f.field_status == 'At Risk'),
        'is_admin': is_admin,
    }
    return render(request, 'fields/dashboard.html', context)