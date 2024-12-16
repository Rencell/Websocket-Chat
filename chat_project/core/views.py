from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from Accounts.models import User
from core.models import Friend, conversation,FriendRequests
from django.db import IntegrityError
from django.db.models import Subquery, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class index(LoginRequiredMixin,ListView):
    model = User
    context_object_name = "users"
    template_name = "core/index.html"
    
    
    def get_friends_ids(self):
        friends = Friend.objects.filter(user1=self.request.user)
        
        if friends.exists():
            friends = Friend.objects.filter(user1=self.request.user).values_list('user2', flat=True)
        else:
            friends = Friend.objects.filter(user2=self.request.user).values_list('user1', flat=True)
        
        return friends
    
    def get_friend_available(self):
        friends_to_add = FriendRequests.objects.filter(user1=self.request.user)
        
        if friends_to_add.exists():
            friends_to_add = FriendRequests.objects.filter(user1=self.request.user).values_list('user2', flat=True)
        else:
            friends_to_add = FriendRequests.objects.filter(user2=self.request.user).values_list('user1', flat=True)
        
        return friends_to_add
    
    def get_queryset(self):
        friends_to_add = self.get_friend_available()
        user = User.objects.exclude(id=self.request.user.id)
        user = user.exclude(id__in=Subquery(friends_to_add))
        return user
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friends = self.get_friends_ids()
        context['already_friends'] = User.objects.filter(id__in=friends)
        return context
    
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('auth')
        
        try:
            # user1 = self.request.user
            # user2 = User.objects.get(id=action)
            # Friend.objects.create(user1=user1, user2=user2)
            
            user2 = self.request.user
            user1 = User.objects.get(id=action)
            FriendRequests.objects.create(user1=user1, user2=user2)
        except IntegrityError:
            messages.error(request, "You are already friends with this user.")
        
        return redirect('core_index')


class conversations(LoginRequiredMixin, ListView):
    
    model = conversation
    template_name = 'core/conversation.html'
    
    def get_friend(self, user2):
        query = Q(user1=self.request.user, user2=user2) | Q(user2=self.request.user, user1=user2)
        return Friend.objects.get(query)
    
    def get_queryset(self):
        sender_id = self.kwargs.get('friend')
        sender = User.objects.get(id=int(sender_id))
        friend = self.get_friend(sender)
        queryset = conversation.objects.filter(friend=friend)
        
        return queryset   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sender_id = self.kwargs.get('friend')
        
        sender = User.objects.get(id=int(sender_id))
        friend = self.get_friend(sender) 
        queryset = conversation.objects.filter(friend=friend)
        
        
        context['conversations'] = queryset
        context['conversation_room'] = friend.id
        context['friend'] = sender
        return context

class PendingRequest(LoginRequiredMixin, ListView):
    model = FriendRequests
    context_object_name = "friendrequests"
    template_name = "core/pending.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = FriendRequests.objects.filter(user1=self.request.user, status="pending")
        return queryset
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('validate')
        auth_id = request.POST.get('auth')
        
        user2 = User.objects.get(id=auth_id)
        friend = FriendRequests.objects.get(user1=self.request.user, user2=user2)
        if action == "accept":
            friend.status = "accepted"
        else:
            friend.status = "denied"
        friend.save()
            
        
        return redirect('core_pending_request')
    


