from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def redirect_to_profile(request):
    profile = request.user.profile
    return redirect('hubspace:profile_page', id = profile.id)
