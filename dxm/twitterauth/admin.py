from django.contrib import admin
from twitterauth.models import UserProfile, Rating

class UserProfileAdmin(admin.ModelAdmin):
    pass

class RatingAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Rating, RatingAdmin)
