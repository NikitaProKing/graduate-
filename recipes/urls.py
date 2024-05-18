from .import views
from django.urls import path

from .views import profile_view, login_view

urlpatterns = [
    path('', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('reg/', views.Reg_View.as_view(), name='reg'),
    path('logout/', views.logout, name='logout'),
    # path('home/', views.Home_View.as_view(), name='home'),
]