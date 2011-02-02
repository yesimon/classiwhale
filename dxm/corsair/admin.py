from django.contrib import admin
from corsair.models import TrainingSet, PredictionStatistics

class TrainingSetAdmin(admin.ModelAdmin):
    pass

class PredictionStatisticsAdmin(admin.ModelAdmin):
    list_display = ('classifier', 'training_set', 'model', 'created')

admin.site.register(TrainingSet, TrainingSetAdmin)
admin.site.register(PredictionStatistics, PredictionStatisticsAdmin)
