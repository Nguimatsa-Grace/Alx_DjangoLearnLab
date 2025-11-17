from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# This is the view that requires authentication
@login_required
def security_home_view(request):
    # This assumes you will create a template at core_security/templates/core_security/home.html
    return render(request, 'core_security/home.html', {})