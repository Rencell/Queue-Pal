import random
import string
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin # type: ignore
from django.urls import reverse_lazy
from core.models import Room, UserRoom, RoomStatus, Status
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
        room = Room.objects.get(code=uid)
        userroom = UserRoom.objects.filter(room=room, queue_number=room.current_serving_queue_number).first()
        if userroom:
            context['userroom'] = userroom
            context['userroom_status'] = userroom.status.pk
        context['Room'] = room
        return context
    
    def post(self, request, *args, **kwargs):
        
        code = self.kwargs.get('code')
        if request.method == 'POST':
            if 'janice' in request.POST:
                roomstatus = RoomStatus.objects.filter(id=2).first()
                room = Room.objects.filter(code=code).first()
                room.status = roomstatus
                reason = request.POST.get('announcement_reason')
                time = request.POST.get('announcement_time')
                room.status_description = f"{reason},{time}"
                room.save()
            # userroom_id = request.POST.get('userroom')
            # userroom = UserRoom.objects.filter(pk=userroom_id).first()
            # userroom.status = Status.objects.get(id=3)
            # userroom.save()
            url = reverse_lazy('staff_queue_room', kwargs={'code': code})
            return redirect(url)
    
    
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
    
    
# -------------------------------
from channels.layers import get_channel_layer
from django.template.loader import get_template
from asgiref.sync import async_to_sync

def htmxtry(request, userroom_id):
    
    if request.method == 'POST':
        userroom = UserRoom.objects.filter(id=userroom_id).first()
        
        if userroom:
            userroom.status = Status.objects.get(id=13)
            userroom.save()
            message_html = get_template('core/partials/countdown.html').render({})
            message_html = message_html.replace('\n', '').replace('\r', '')
            room =  f'{userroom.room.code}_{userroom.user.username}'
            channel_layer = get_channel_layer()
            
            async_to_sync(channel_layer.group_send)(
                room,
                {
                    'type' : 'queue_number',
                    'message' : message_html
                }
            )
            return HttpResponse("<div id='tim' hx-swap-oob='true'>Timer</div>")
        
        return HttpResponse("<div id='lol' hx-swap-oob='true'>No user found</div>")
        



def appoint_user(request, userroom_id):
    
    userroom = UserRoom.objects.filter(id=userroom_id).first()
    if userroom:
        userroom.status = Status.objects.get(id=2)
        userroom.save()
        return HttpResponse("<div id='appoint' hx-swap-oob='true'>Appointed</div>")
    return HttpResponse("<div id='appoint' hx-swap-oob='true'>No user found</div>")

def noshow_user(request, userroom_id):
    
    userroom = UserRoom.objects.filter(id=userroom_id).first()
    if userroom:
        userroom.status = Status.objects.get(id=4)
        userroom.save()
        return HttpResponse("<div id='noshow' hx-swap-oob='true'>No Showed</div>")
    return HttpResponse("<div id='noshow' hx-swap-oob='true'>No user found</div>")
    