from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index.as_view(), name="core_index"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('pendingrequest', views.PendingRequest.as_view(), name='core_pending_request'),
    path('<str:friend>/conversation', views.conversations.as_view(), name='core_conversation')
    
]