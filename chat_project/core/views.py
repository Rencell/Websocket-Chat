from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from Accounts.models import User
from core.models import Friend, conversation
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
    
    def get_queryset(self):
        friends = self.get_friends_ids()
        return User.objects.exclude(id=self.request.user.id).exclude(id__in=Subquery(friends))
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friends = self.get_friends_ids()
        context['already_friends'] = User.objects.filter(id__in=friends)
        return context
    
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('auth')
        
        try:
            user1 = self.request.user
            user2 = User.objects.get(id=action)
            Friend.objects.create(user1=user1, user2=user2)
        except IntegrityError:
            messages.error(request, "You are already friends with this user.")
        
        return redirect('core_index')


class conversations(LoginRequiredMixin, ListView):
    
    model = conversation
    template_name = 'core/conversation.html'
    
    def get_queryset(self):
        param = self.kwargs.get('param')
        user2 = User.objects.get(id=int(param))
        friend = Friend.objects.get(Q(user1=self.request.user, user2=user2) 
                                    | Q(user2=self.request.user, user1=user2))
        queryset = conversation.objects.filter(friend=friend)
        
        return queryset
   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        param = self.kwargs.get('param')
        
        user2 = User.objects.get(id=int(param))
        friend = Friend.objects.get(Q(user1=self.request.user, user2=user2) 
                                    | Q(user2=self.request.user, user1=user2))
        queryset = conversation.objects.filter(friend=friend)
        
        
        context['conversations'] = queryset
        context['param'] = friend.id
        context['friend'] = param
        return context
    


