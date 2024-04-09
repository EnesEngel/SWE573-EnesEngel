from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('create/', views.create_user, name='create_user'),
]
