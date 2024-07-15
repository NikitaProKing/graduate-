from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.checks import messages
from django.db import transaction
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, FormView, DeleteView
from django.core.paginator import Paginator
from .forms import LoginForm, RegForm, Add_a_recipe_Form, CommentForm, DetailForm, SubscribeForm, UnsubscribeForm
from .models import Profile, VisitedPage, Home_Model, Add_a_recipe_Model, CommentModel, Detail_Model, Favorite, \
    Subscription


@login_required
def profile_view(request):
    products_count = Add_a_recipe_Model.objects.filter(author=request.user).count()
    product = Add_a_recipe_Model.objects.all ().filter(author=request.user)
    return render(request, 'profile.html', {'products_count': products_count, 'product': product})


@login_required
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

@login_required
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
        edit = Add_a_recipe_Form(request.POST, request.FILES, instance=recipes)
        if edit.is_valid():
            edit.save()
            return redirect('edit_recipes.html', recipes_id=recipes.id)
    else:
        edit = Add_a_recipe_Form(instance=recipes)
    return render(request, 'edit_recipes.html', {'edit': edit})


def commentView(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.save()
            return redirect('post_detail')
    else:
        form = CommentForm()

    return render(request, 'comment.html', {'form': form})


class MyDetailView(DetailView):
    model = Detail_Model
    template_name = 'detail.html'
    context_object_name = 'detail'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


def upload_image(request):
    if request.method == 'POST':
        form = DetailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile.url')
    else:
        form = DetailForm()
    return render(request, 'detail.html', {'form': form})


# class CreatePostView(FormView):
#     form_class = PostForm
#     template_name = 'post.html'
#     success_url = reverse_lazy('home')
#     def form_valid(self, form):
#         form.save(commit=False)
#         for item in self.request.FILES.getlist('image'):
#             Post.objects.create(image=item, author=self.request.user)
#             return super().form_valid(form)


class AddDetailView(CreateView):
    model = Detail_Model
    template_name = 'add_detail.html'
    form_class = DetailForm
    success_url = reverse_lazy('profile')
    context_object_name = 'form'

    from django.db import transaction

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            return HttpResponse("Пожалуйста, войдите в систему для добавления деталей")

        title_id = self.kwargs.get('recipes_id')
        try:
            title_instance = Add_a_recipe_Model.objects.get(id=title_id)
        except Add_a_recipe_Model.DoesNotExist:
            return HttpResponseNotFound("Рецепт не найден")

        with transaction.atomic():
            texts = self.request.POST.getlist('text[]')
            print(texts)
            photos = self.request.FILES.getlist('photo[]')
            for text, photo in zip(texts, photos):
                Detail_Model.objects.create(
                    text=text,
                    photo=photo,
                    author=self.request.user,
                    title=title_instance
                )

        return redirect('profile')


class MyDeleteView(DeleteView):
    model = Add_a_recipe_Model
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_context'] = 'some_value'
        return context

# class Add_Detail_Delete_View(DeleteView):

@login_required
@require_POST
def add_to_favoritesView(request, item_id):
    item = Add_a_recipe_Model.objects.get(id=item_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, item=item)

    if created:
        return HttpResponse('Товар добавлен в избранное')
    else:
        return HttpResponse('Товар уже в избранном')


@login_required
def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            return redirect('subscriptions')
    else:
        form = SubscribeForm()
    return render(request, 'subscribe.html', {'form': form})

@login_required
def unsubscribe(request):
    if request.method == 'POST':
        form = UnsubscribeForm(request.POST)
        if form.is_valid():
            subscribed_to = form.cleaned_data['subscribed_to']
            subscription = get_object_or_404(Subscription, user=request.user, subscribed_to=subscribed_to)
            subscription.delete()
            return redirect('subscriptions')
    else:
        form = UnsubscribeForm()
    return render(request, 'unsubscribe.html', {'form': form})

@login_required
def subscriptions_list(request):
    subscriptions = Subscription.objects.filter(user=request.user)
    return render(request, 'subscriptions_list.html', {'subscriptions': subscriptions})