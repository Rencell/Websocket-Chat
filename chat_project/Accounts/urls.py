from django.urls import path,include
from . import views
urlpatterns = [
    path('', include('django.contrib.auth.urls'), name="login"),
    path('register/', views.registerUser.as_view(), name="register")
]