from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login

from .forms import LoginForm, RegForm


@login_required
def profile_view(request):
    return render(request, 'templates/profile.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
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
            form.save()
            return redirect('login')
    else:
        form = RegForm()
    return render(request, 'registration/reg.html', {'form': form})
