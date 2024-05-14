from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login

from .forms import LoginForm, RegForm
from .models import Profile, VisitedPage


@login_required
def profile_view(request):
    return render(request, 'templates/profile.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['useremail']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль. Пожалуйста, попробуйте снова.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def reg_view(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('login')
    else:
        form = RegForm()
    return render(request, 'registration/reg.html', {'form': form})

def logout(request):
    if request.user.is_authenticated:
        visited_pages = []
        visited_cookies = request.COOKIES.get('visit_count')
        if visited_cookies:
            visited_pages = visited_cookies.split(',')
            for page in visited_pages:
                VisitedPage.objects.create(user=request.user, page_name=page)
            response = redirect('create_form')
            response.delete_cookie('visit_count')
            return response
    else:
        return redirect('create_form')