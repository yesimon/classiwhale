from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from twitterauth.models import UserProfile, Rating

class UserProfileInline(admin.TabularInline):
    model = UserProfile
    fk_name = 'user'
    max_num = 1


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline,]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    
#    def twitter_screen_name(self, obj):
#        return obj.get_profile().screen_name

class RatingAdmin(admin.ModelAdmin):
    pass

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Rating, RatingAdmin)
