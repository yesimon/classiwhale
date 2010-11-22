from django.contrib import admin
from status.models import Status, Hashtag, Hyperlink


class StatusAdmin(admin.ModelAdmin):
    pass

admin.site.register(Status, StatusAdmin)

