from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError 
# Create your models here.

    


USER_ACTIVITY_CHOISES = (
    ('checkin', 'Check In'),
    ('checkout', 'Check Out'),
)


class UserActivityManager(models.Manager):
    def current(self, user = None):
        if user is None:
            return None
        current_obj = self.get_queryset().filter(user=user).order_by('-timestamp').first()
        return current_obj
    def toggle(self, user = None):
        if user is None:
            return None
        last_item = self.current(user)
        activity = "checkin"
        if last_item is not None:
            if last_item.activity == "checkin":
                activity = "checkout"
        obj = self.model(user = user, activity = activity)
        obj.save()   
        return obj 


class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    activity = models.CharField(max_length=120, default='checkin', choices= USER_ACTIVITY_CHOISES)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
    objects = UserActivityManager()
    def __str__ (self):
        return str(self.activity)

    class Meta: 
        verbose_name = 'activity'
 
    def clean(self, *args, **kwargs):
        if self.user:
            user_activities = UserActivity.objects.exclude(id = self.id).filter(user = self.user).order_by('-timestamp')
            if user_activities.exists():
                recent_ = user_activities.first()
                if self.activity == recent_.activity:
                    message= "%s is not a valid avtivity for these user." % (self.get_activity_display())

                    raise ValidationError(message)
            else:
                if self.activity != "checkin":
                   message= "%s is not a valid avtivity for these user as a first activity." % (self.get_activity_display()) 
                   raise ValidationError(message)
            
            return super(UserActivity,self).clean(*args,**kwargs)
                    