from .import views
from django.urls import path

from .views import profile_view, login_view, reg_view

urlpatterns = [
    path('', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('reg/', views.reg_view, name='reg'),
]