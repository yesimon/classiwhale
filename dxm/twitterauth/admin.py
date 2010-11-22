from django.contrib import admin
from twitterauth.models import UserProfile, RatingDetails

class UserProfileAdmin(admin.ModelAdmin):
    pass

class RatingDetailsAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(RatingDetails, RatingDetailsAdmin)
