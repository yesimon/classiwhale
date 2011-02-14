from django.contrib import admin
from corsair.models import TwitterTrainingSet, PredictionStatistics

class TwitterTrainingSetAdmin(admin.ModelAdmin):
    pass

class PredictionStatisticsAdmin(admin.ModelAdmin):
    list_display = ('classifier', 'training_set', 'model', 'created')

admin.site.register(TwitterTrainingSet, TwitterTrainingSetAdmin)
admin.site.register(PredictionStatistics, PredictionStatisticsAdmin)
