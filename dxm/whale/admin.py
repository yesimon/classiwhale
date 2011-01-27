from django.contrib import admin
from whale.models import Whale, WhaleSpecies


class WhaleAdmin(admin.ModelAdmin):
    pass

class WhaleSpeciesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Whale, WhaleAdmin)
admin.site.register(WhaleSpecies, WhaleSpeciesAdmin)
