import random
import string
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin # type: ignore
from django.urls import reverse_lazy
from core.models import Room, UserRoom, RoomStatus
from datetime import date

class user_index(GroupRequiredMixin, TemplateView):
    
    
    
    login_url = reverse_lazy("login")
    group_required = ['Staff', 'admin']
    template_name = "staff/index.html"
    raise_exception = True
    
    def post(self, request, *args, **kwargs):
        uid = str(''.join(random.choices(string.ascii_letters + string.digits, k=4))).upper()
        Room.objects.create(staff=request.user, code=uid)
        return redirect(reverse_lazy('staff_queue_room', kwargs={'code': uid}))
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        today = date.today()
        try:
            check_room = Room.objects.get(staff=self.request.user, created_at__date=today)
        except Room.DoesNotExist:
            check_room = Room.objects.none()

        
        context['available'] = check_room
        return context
    
    
    
class room_view(GroupRequiredMixin, ListView):
    model=UserRoom
    template_name = "staff/room.html"
    group_required = ['Staff', 'admin']
    login_url = reverse_lazy("login")
    context_object_name="rooms"
    
    
    def get_queryset(self):
        queryset = super().get_queryset()
        uid = self.kwargs.get('code')
        room = Room.objects.get(code=uid)
        queryset = UserRoom.objects.filter(room=room)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uid = self.kwargs.get('code')
        
        context['Room'] = Room.objects.get(code=uid)
        return context
    
    
class store_customer(GroupRequiredMixin, CreateView):
    
    model= UserRoom
    template_name = "staff/create_customer.html"
    fields = ['user', 'room', 'status']
    group_required = ['Staff', 'admin']
    
    def get_success_url(self):
        return reverse_lazy('staff_queue_room', kwargs={'code': self.kwargs.get('code')})
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['code'] =  self.kwargs.get('code')
        return context
    
class destroy_customer(GroupRequiredMixin, DeleteView):
    
    model= UserRoom
    template_name = "staff/userroom_confirm_delete.html"
    group_required = ['Staff', 'admin']
    
    def get_success_url(self):
        return reverse_lazy('staff_queue_room', kwargs={'code': self.kwargs.get('code')})
    
    
    