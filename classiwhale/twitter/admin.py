from django.contrib import admin
from twitter.models import Status, Rating, TwitterUserProfile


class TwitterStatusAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('id', 'user', 'text', 'created_at')

class TwitterRatingAdmin(admin.ModelAdmin):
    pass

class TwitterUserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Status, TwitterStatusAdmin)
admin.site.register(Rating, TwitterRatingAdmin)
admin.site.register(TwitterUserProfile, TwitterUserProfileAdmin)

