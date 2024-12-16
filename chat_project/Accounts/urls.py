from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.home.as_view(), name="home"),
    path('', include('django.contrib.auth.urls'), name="login"),
    path('register/', views.registerUser.as_view(), name="register")
]