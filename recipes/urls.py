from django.views.generic import DeleteView

from .import views
from django.urls import path

from .views import profile_view, login_view, MyDeleteView

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('reg/', views.Reg_View.as_view(), name='reg'),
    path('logout/', views.logout_view, name='logout'),
    path('recipes_list/', views.recipes_list, name='recipes_list'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('comment/', views.commentView, name='comment'),
    # path('Detail/<slug:slug>/', views.MyDetailView.as_view(), name='detail1'),
    # path('detail/<int:pk>', views.detail, name='detail'),
    path('addDetail/<int:recipes_id>', views.AddDetailView.as_view(), name='addDetail'),
    path('edit_recipes/<int:recipes_id>', views. edit_recipes, name='edit_recipes'),
    # path('favorite/', views.favorite_view, name='favorite'),
    path('Delete/<int:pk>/', MyDeleteView.as_view(), name='Delete-delete')
]

