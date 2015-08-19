from django.contrib import admin

from .models import TempData, User

class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User

class TempDataAdmin(admin.ModelAdmin):
    class Meta:
        model = TempData
        
admin.site.register(User, UserAdmin)
admin.site.register(TempData, TempDataAdmin)