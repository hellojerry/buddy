from django.contrib import admin

from .models import Activity

class ActivityAdmin(admin.ModelAdmin):
    class Meta:
        model = Activity
        
admin.site.register(Activity, ActivityAdmin)
