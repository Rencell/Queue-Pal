from django.forms import ValidationError
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Settings(models.Model):
    notificationEnabled = models.BooleanField(default=True)
    summon_queue_number = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.summon_queue_number

class Status(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Issue(models.Model):
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
    

class RoomStatus(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Room(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True) 
    current_serving_queue_number = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(RoomStatus, on_delete=models.CASCADE, default=1)

    class Meta:
        unique_together = ['staff', 'code']
     
    def validate(self):
        today = timezone.now().date()
        if Room.objects.filter(staff=self.staff, created_at__date=today).exists():
            raise ValidationError("A room has already been created for this staff today.")

    def save(self, *args, **kwargs):
        self.validate() 
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.code
    
class UserRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="Anonymous", null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, null=True, blank=True) 
    queue_number = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'room']
        
    def save(self, *args, **kwargs):
        
        roomcount = UserRoom.objects.filter(room=self.room).count()
        roomcount += 1
        self.queue_number = roomcount
        
        super().save(*args, **kwargs)

    

    