from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views.generic import TemplateView,ListView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin # type: ignore
from django.urls import reverse_lazy
from core.models import Room, Status, UserRoom, Issue, RoomStatus

class index(LoginRequiredMixin, TemplateView):
    template_name = "core/bitch.html"
    
    # Status.objects.create(name="PENDING", description="default pending")
    # Status.objects.create(name="SERVING", description="current serving")
    # Status.objects.create(name="CANCELLED", description="ended session or cancelled")
    # Status.objects.create(name="NO_SHOW", description="did not show")
    
    # RoomStatus.objects.create(name="ACTIVE")
    # RoomStatus.objects.create(name="PAUSED")
    # RoomStatus.objects.create(name="TERMINATED")
    
    def post(self, request, *args, **kwargs):
        user_room = str(request.POST.get('user_room')).upper()
        try:
            room = Room.objects.get(code=user_room)
            if room:
                return redirect(reverse_lazy('core_issue', kwargs={'code': user_room}))
        except Exception as e:
            messages.error(request,e)
        return redirect(reverse_lazy('core_index'))

class issue_view(LoginRequiredMixin, TemplateView):
    template_name="core/issue.html"
    
    def post(self, request, *args, **kwargs):
        user_issue = str(request.POST.get('issue'))
        room_code = str(self.kwargs.get('code'))
        try:
            issue = Issue.objects.create(description=user_issue)
            room = Room.objects.get(code=room_code)
            if room:
                userroom, created = UserRoom.objects.get_or_create(
                    user=request.user,
                    room=room,
                    issue=issue
                )
                if created:
                    request.session['userroom'] = userroom.id
                    
                return redirect(reverse_lazy('core_queue'))
        except IntegrityError as e:
            userroom = UserRoom.objects.get(user=request.user, room=room)
            request.session['userroom'] = userroom.id
            
            return redirect(reverse_lazy('core_queue'))
            
        except Exception as e:
            messages.error(request,e)
            
        return redirect(reverse_lazy('core_issue', kwargs={'code': room_code}))
    
class queue_view(LoginRequiredMixin, ListView):
    model = UserRoom
    template_name = "core/Queue.html"
    context_object_name = "room"
    
    def get_queryset(self):
        userroom_id = self.request.session.get('userroom')
        query_set = UserRoom.objects.get(id=userroom_id)
        
        return query_set
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.get_queryset().room
        context['room_code'] = room.code
        context['current_serving'] = room.current_serving_queue_number
        
        return context

    def post(self, request, *args, **kwargs):
        # Cancelling the Queue
        CANCEL_STATUS = Status.objects.get(id=3) 
        userroom_id = self.request.session.get('userroom')
        query_set = UserRoom.objects.get(id=userroom_id)
        query_set.status = CANCEL_STATUS
        query_set.save()
        
        return redirect(reverse_lazy('core_cancelled'))
    

class closing_view(LoginRequiredMixin, TemplateView):
    template_name = "core/salutation.html"

