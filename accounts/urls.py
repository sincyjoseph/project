from accounts.views import sample
from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.home, name='home'), 
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('sample', views.sample, name='sample'),
    path('adminpage', views.adminpage, name='adminpage'),
    path('search-userdetails', csrf_exempt(views.search_userdetails), name='search_userdetails'),
    path('dashboard/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('dashboard/<int:pk>/delete/', views.UserDetailDeleteView, name='user_detaildelete'),
]
