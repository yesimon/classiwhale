from django.contrib import admin
from corsair.models import TrainingSet, PredictionStatistics

class TrainingSetAdmin(admin.ModelAdmin):
    pass

class PredictionStatisticsAdmin(admin.ModelAdmin):
    pass

admin.site.register(TrainingSet, TrainingSetAdmin)
admin.site.register(PredictionStatistics, PredictionStatisticsAdmin)
