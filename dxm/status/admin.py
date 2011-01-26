from django.contrib import admin
from status.models import Status, Hashtag, Hyperlink


class StatusAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('id', 'user_profile', 'text', 'created_at')

admin.site.register(Status, StatusAdmin)

