from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def profile_view(request):
    return render(request, 'templates/profile.html')

def login_view(request):
    return render(request, 'registration/login.html')


