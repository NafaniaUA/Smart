

from django.contrib import admin
from .models import UserActivity

# Register your models here.


class UserActivityAdmin (admin.ModelAdmin):
    search_fields = ['user__username', 'user__email']
    list_display = ['user','timestamp','activity']

   
admin.site.register(UserActivity, UserActivityAdmin)