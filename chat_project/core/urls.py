from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index.as_view(), name="core_index"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create-room/', views.createRoom.as_view(), name='core_create'),
    path('join-room/', views.joinRoom, name='core_join'),
    path('room/<str:slug>', views.room, name='core_tara'),
    
]