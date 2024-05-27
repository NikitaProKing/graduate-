from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.checks import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.paginator import Paginator
from .forms import LoginForm, RegForm, Add_a_recipe_Form, CommentForm
from .models import Profile, VisitedPage, Home_Model, Add_a_recipe_Model, CommentModel


@login_required
def profile_view(request):
    return render(request, 'profile.html')


def add_recipe(request):
    if request.method == 'POST':
        form = Add_a_recipe_Form(request.POST, request.FILES)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            new_recipe.save()

            return redirect('profile')
    else:
        form = Add_a_recipe_Form()

    return render(request, 'Add_a_recipe.html', {'form': form})
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
    my_queryset = Add_a_recipe_Model.objects.all()
    paginator = Paginator(my_queryset, 25)
    page = request.GET.get('page')
    my_objects = paginator.get_page(page)
    return render(request, 'home.html', {'my_objects': my_objects})

def recipes_list(request):
    recipes = Add_a_recipe_Model.objects.filter(is_published=True)
    return render(request, 'Add_a_recipe.html', {'recipes': recipes})


class Add_Views(CreateView):
    model = Add_a_recipe_Model
    template_name = 'Add_a_recipe.html'
    form_class = Add_a_recipe_Form
    success_url = reverse_lazy('profile')
    context_object_name = 'form'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

@login_required
def edit_recipes(request, recipes_id):
    recipes = get_object_or_404(Add_a_recipe_Model, id=recipes_id)
    if request.user != recipes.author:
        return HttpResponse('You are not allowed to edit this recipe.')
    if request.method == 'POST':
        form = Add_a_recipe_Form(request.POST, request.FILES, instance=recipes)
        if form.is_valid():
            form.save()
            return redirect('recipes_detail', recipes_id=recipes.id)
    else:
        form = Add_a_recipe_Form(instance=recipes)
    return render(request, 'edit_recipe.html', {'form': form})


def commentView(request, post_id):
    post = get_object_or_404(CommentModel, id=post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'comment.html', {'post': post, 'comments': comments, 'form': form})