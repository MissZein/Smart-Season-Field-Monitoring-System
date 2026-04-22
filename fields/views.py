from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Field
from django.http import HttpResponse
from django.template.loader import render_to_string

@login_required
def update_field_status(request, pk):
    field = get_object_or_404(Field, pk=pk)
    
    # Check if the user is the assigned agent or an admin
    if field.assigned_agent == request.user or request.user.is_superuser:
        if request.method == "POST":
            new_stage = request.POST.get('current_stage')
            field.current_stage = new_stage
            field.save()
            
            # Return just the updated card to the frontend
            html = render_to_string('fields/partials/field_card.html', {'field': field, 'user': request.user})
            return HttpResponse(html)
    
    return HttpResponse("Unauthorized", status=403)
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
# 1. This view returns the HTML for the input box
@login_required
def edit_notes(request, pk):
    field = get_object_or_404(Field, pk=pk)
    return HttpResponse(f'''
        <form hx-post="/save-notes/{field.id}/" hx-target="this" hx-swap="outerHTML">
            <textarea name="notes" rows="3" style="width:100%">{field.notes or ''}</textarea>
            <button type="submit">Save</button>
            <button hx-get="/get-notes/{field.id}/">Cancel</button>
        </form>
    ''')

# 2. This view saves the data
@login_required
def save_notes(request, pk):
    field = get_object_or_404(Field, pk=pk)
    if request.method == "POST":
        field.notes = request.POST.get('notes')
        field.save()
    # Return to the regular display mode
    return render(request, 'fields/partials/field_card.html', {'field': field})