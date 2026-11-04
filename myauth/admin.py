from django.contrib import admin

from myauth.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = 'user',
    list_display_links = 'user',
