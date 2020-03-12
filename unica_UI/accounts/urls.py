from django.urls import path
from . import views

urlpatterns = [
    path('', views.login2, name='login2'),
    path('register', views.register,name='register'),
    path('logout',views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard')
]