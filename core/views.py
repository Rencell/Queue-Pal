from datetime import date, timedelta
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView,ListView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin # type: ignore
from django.urls import reverse_lazy
from core.models import Room, Status, UserRoom, Issue, RoomStatus
class index(LoginRequiredMixin, TemplateView):
    template_name = "core/index.html"
    
    def post(self, request, *args, **kwargs):
        user_room = str(request.POST.get('user_room')).upper()
        
        try:
            ACTIVE = 1 
            TERMINATED = 3
            room = Room.objects.filter(code=user_room).first()
            
            if room.status.id == ACTIVE:
                return redirect(reverse_lazy('core_issue', kwargs={'code': user_room}))
            elif room.status.id == TERMINATED:
                messages.error(request,"The room has already been terminated")
        except Exception as e:
            messages.error(request,e)
        return redirect(reverse_lazy('core_index'))
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        today = date.today()
        
        try:
            status = Status.objects.filter(id__in=[1,5])
            isSession = UserRoom.objects.get(user=self.request.user, created_at__date=today, status__in=status)
            
            context['current_serving'] = isSession.room.current_serving_queue_number
            context['queue_number'] = isSession.queue_number
            self.request.session['userroom'] = isSession.pk
        except UserRoom.DoesNotExist:
            isSession = False
        
        
        context['isSession'] = isSession
        return context


class issue_view(LoginRequiredMixin, TemplateView):
    template_name="core/issue.html"
    
    def post(self, request, *args, **kwargs):
        user_issue = str(request.POST.get('issue'))
        room_code = str(self.kwargs.get('code'))
        try:
            room = Room.objects.get(code=room_code)
            
            if room:
                PENDING = 1
                status = Status.objects.filter(id=PENDING).first()
                
                userroom = UserRoom.objects.filter(
                    user=request.user,
                    room=room,
                    status=status
                ).first()
                
                if not userroom:
                    issue = Issue.objects.create(description=user_issue)
                    userroom = UserRoom.objects.create(
                    user=request.user,
                    room=room,
                    issue=issue,
                    status=status
                )
                request.session['userroom'] = userroom.id
                
                
                    
                return redirect(reverse_lazy('core_queue'))
        except IntegrityError as e:
            userroom = UserRoom.objects.get(user=request.user, room=room)
            request.session['userroom'] = userroom.id
            
            return redirect(reverse_lazy('core_queue'))
            
        except Exception as e:
            
            messages.error(request,e)
            
        return redirect(reverse_lazy('core_issue', kwargs={'code': room_code}))

import re
from datetime import datetime, timedelta
class queue_view(LoginRequiredMixin, ListView):
    model = UserRoom
    template_name = "core/Queue.html"
    context_object_name = "userroom"
    
    
    def get_userroom(self):
        userroom_id = self.request.session.get('userroom')
        userroom = UserRoom.objects.get(id=userroom_id)
        
        return userroom
    
    def get_queryset(self):
        query_set = self.get_userroom()
        return query_set
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.get_queryset().room
        userroom = self.get_userroom()
        
        context['room'] = room
        context['room_code'] = room.code
        context['userroom_status'] = userroom.status.pk
        context['current_serving'] = room.current_serving_queue_number
        
        return context
        

    def get(self, request, *args, **kwargs):
        userroom_id = request.session.get('userroom')
        
        if userroom_id:
            try:
                userroom = UserRoom.objects.get(id=userroom_id)
                return super().get(request, *args, **kwargs)
            except UserRoom.DoesNotExist:
                return redirect(reverse_lazy('core_queue_error'))
        else:
            return redirect(reverse_lazy('core_queue_error'))
        
    def post(self, request, *args, **kwargs):
        if 'cancel_session' in request.POST:
            CANCEL_STATUS = Status.objects.get(id=3) 
            query_set = self.get_userroom()
            query_set.status = CANCEL_STATUS
            query_set.save()
            del request.session['userroom'] 
        elif 'back_home' in request.POST:
            
            del request.session['userroom'] 
            return redirect(reverse_lazy('core_index'))

        
        return redirect(reverse_lazy('core_cancelled'))
    

class queue_error(LoginRequiredMixin, TemplateView):
    template_name = "core/error/backHome.html"
    
class closing_view(LoginRequiredMixin, TemplateView):
    template_name = "core/salutation.html"
    

