from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from core.models import Room, Message
from django.contrib.auth.decorators import login_required

class index(LoginRequiredMixin,TemplateView):
    template_name = "core/index.html"
    

class createRoom(LoginRequiredMixin, CreateView):
    model = Room
    template_name = "core/create-room.html"
    fields = ['name'] 
    success_url = reverse_lazy("core_index")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.users.add(self.request.user)
        
        return response

@login_required   
def joinRoom(request):
    
    if request.method == "POST":
        room = request.POST['room']
        room_query = Room.objects.get(slug=room)
        return redirect(reverse('core_tara', kwargs={'slug': room_query.slug}))
    return render(request, 'core/join-room.html')

@login_required 
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)
    return render(request, 'core/real-room.html', {'name': room.name, 'slug': room.slug, 'messages' : messages})