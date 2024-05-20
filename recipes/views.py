from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.paginator import Paginator
from .forms import LoginForm, RegForm
from .models import Profile, VisitedPage, Home_Model


@login_required
def profile_view(request):
    return render(request, 'profile.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('profile')
            else:
                return render(request, 'registration/login.html', {'form': form, 'error': 'Неверный адрес электронной почты или пароль'})
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


class Reg_View(CreateView):
    model = User
    template_name = 'registration/reg.html'
    form_class = RegForm
    success_url = reverse_lazy('login')
    context_object_name = 'form'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('/')

def home_view(request):
    my_queryset = Home_Model.objects.all()
    paginator = Paginator(my_queryset, 25)
    page = request.GET.get('page')
    my_objects = paginator.get_page(page)
    return render(request, 'home.html', {'my_objects': my_objects})