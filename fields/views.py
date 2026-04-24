from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Field
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.utils import timezone

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
        fields = Field.objects.all().select_related('assigned_agent')
        # This list powers your dropdowns!
        all_agents = User.objects.filter(is_staff=True) 
    else:
        fields = Field.objects.filter(assigned_agent=request.user)
        all_agents = None

    # Simple summaries for the dashboard [cite: 50, 52]
    context = {
        'fields': fields,
        'total_fields': fields.count(),
        'at_risk_count': sum(1 for f in fields if f.field_status == 'At Risk'),
        'is_admin': is_admin,
        'all_agents': all_agents,
    }
    return render(request, 'fields/dashboard.html', context)
# 1. This view returns the HTML for the input box
@login_required
def edit_notes(request, pk):
    field = get_object_or_404(Field, pk=pk)
    # This returns a small inline form that fits inside the table cell
    return HttpResponse(f'''
        <form hx-post="/save-notes/{field.id}/" hx-target="#field-row-{field.id}" hx-swap="outerHTML" style="display:flex; gap:5px;">
            <input type="text" name="notes" value="{field.notes or ''}" style="width:100px;">
            <button type="submit" style="background:green; color:white; border:none; padding:2px 5px;">ok</button>
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

@login_required
def assign_agent(request, pk):
    # Check if the user is a Coordinator (Superuser or Staff)
    is_admin = request.user.is_superuser or request.user.is_staff
    if not is_admin:
        return HttpResponse("Unauthorized", status=403)

    field = get_object_or_404(Field, pk=pk)
    
    if request.method == "POST":
        agent_id = request.POST.get('agent_id')
        if agent_id:
            agent = get_object_or_404(User, id=agent_id)
            field.assigned_agent = agent
        else:
            field.assigned_agent = None # Handle unassigning
        field.save()

    # We need to pass back the context required by the partial row
    all_agents = User.objects.filter(is_superuser=False, is_staff=False)
    
    return render(request, 'fields/partials/field_card.html', {
        'field': field,
        'is_admin': is_admin,
        'all_agents': all_agents
    })

@login_required
def add_field(request):
    if not (request.user.is_superuser or request.user.is_staff):
        return HttpResponse("Unauthorized", status=403)
    
    agents = User.objects.filter(is_superuser=False, is_staff=True)
    # We return a simple HTML modal
    return render(request, 'fields/partials/add_field_modal.html', {'agents': agents})

# Logic to Save the Field
@require_POST
def save_new_field(request):
    name = request.POST.get('name')
    crop = request.POST.get('crop')
    date = request.POST.get('date')
    agent_id = request.POST.get('agent_id')
    
    agent = User.objects.get(id=agent_id) if agent_id else None
    
    Field.objects.create(
        name=name,
        crop_type=crop,
        planting_date=date,
        assigned_agent=agent,
        current_stage='PL' # Default to Planted
    )
    return redirect('dashboard')

# View to show the Add Agent Form
@login_required
def add_agent(request):
    return render(request, 'fields/partials/add_agent_modal.html')

# Logic to Save the Agent
@require_POST
def save_new_agent(request):
    user_name = request.POST.get('username')
    pass_word = request.POST.get('password')
    # Create the user as a regular agent (not staff)
    if user_name and pass_word:
            # Create the user and set is_staff to True automatically
            user = User.objects.create_user(username=user_name, password=pass_word)
            user.is_staff = True 
            user.save()
            
    return redirect('dashboard')

@login_required
def save_new_field(request):
    if request.method == "POST":
        name = request.POST.get('name')
        crop = request.POST.get('crop')
        date_str = request.POST.get('date')
        agent_id = request.POST.get('agent_id')
        print(f"DEBUG: Received Agent ID: {agent_id}")
        # Create the object
        new_field = Field(
            name=name,
            crop_type=crop,
            planting_date=date_str if date_str else timezone.now().date(),
            current_stage='PL'
        )
        
        # Only try to assign if agent_id is not empty/none
        if agent_id and agent_id.strip():
            new_field.assigned_agent_id = int(agent_id) # Using _id is more direct
            
        new_field.save()
    return redirect('dashboard')

@login_required
def save_new_agent(request):
    if request.method == "POST":
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        
        if user_name and pass_word:
            # Create a real User in the Django database
            User.objects.create_user(username=user_name, password=pass_word)
            
    return redirect('dashboard')