from django.contrib import admin
from .models import User
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('id',)