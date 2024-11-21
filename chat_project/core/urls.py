from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index.as_view(), name="core_index"),
    path('logout/', LogoutView.as_view(), name='logout')
    
]