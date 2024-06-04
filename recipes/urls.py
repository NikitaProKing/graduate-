from .import views
from django.urls import path

from .views import profile_view, login_view

urlpatterns = [
    path('', views.home_view, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('reg/', views.Reg_View.as_view(), name='reg'),
    path('logout/', views.logout_view, name='logout'),
    path('recipes_list/', views.recipes_list, name='recipes_list'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('comment/', views.commentView, name='comment'),
    path('detail/', views.product_detail, name='detail'),
    path()
]
