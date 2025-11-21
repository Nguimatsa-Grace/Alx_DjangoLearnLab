from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse 
from .models import Project
from django.contrib.auth.models import User

# --- Helper function to simplify response for testing ---
# We use this instead of rendering full templates
def _simulate_action(request, project=None, action_type=''):
    user = request.user
    project_title = project.title if project else "N/A"
    
    response_content = f"""
    <h1>Permission Granted: {action_type.upper()}</h1>
    <p>User: <strong>{user.username}</strong></p>
    <p>Required Permission: access_control.{action_type.lower().replace(' ', '_')}</p>
    <p>Your current groups: {', '.join(g.name for g in user.groups.all())}</p>
    <p>Target Project: {project_title}</p>
    """
    return HttpResponse(response_content, status=200)


# The full permission string is '<app_label>.<permission_codename>'

@permission_required('access_control.can_view', raise_exception=True)
def project_list(request):
    """View protected by 'can_view'."""
    projects = Project.objects.all() 
    return _simulate_action(request, action_type='Can View')

@permission_required('access_control.can_create', raise_exception=True)
def project_create(request):
    """View protected by 'can_create'."""
    if request.method == 'POST':
        # Simple creation logic
        Project.objects.create(
            title=request.POST.get('title', 'New Project - Test'),
            description='Created via test view.',
            created_by=request.user if request.user.is_authenticated else User.objects.first()
        )
        return redirect('access_control:project_list')
    
    return _simulate_action(request, action_type='Can Create')


@permission_required('access_control.can_edit', raise_exception=True)
def project_edit(request, pk):
    """View protected by 'can_edit'."""
    project = get_object_or_404(Project, pk=pk)
    # Simple edit logic
    return _simulate_action(request, project, action_type=f'Can Edit')

@permission_required('access_control.can_delete', raise_exception=True)
def project_delete(request, pk):
    """View protected by 'can_delete'."""
    project = get_object_or_404(Project, pk=pk)
    # Simple delete logic
    return _simulate_action(request, project, action_type=f'Can Delete')