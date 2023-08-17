from django.contrib import admin

from core.admin import BaseAdmin
from users.models import Subscribe, User


@admin.register(User)
class UserAdmin(BaseAdmin):
    list_display = ('pk', 'email', 'username', 'first_name', 'last_name')
    list_filter = ('username',)
    search_fields = ('username',)


@admin.register(Subscribe)
class FollowAdmin(BaseAdmin):
    list_display = ('pk', '__str__')
    search_fields = ('user',)
