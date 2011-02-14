from celery.decorators import task
from corsair.models import TwitterTrainingSet

@task
def benchmark(training_set_name, classifier):
   t = TwitterTrainingSet.objects.get(name=training_set_name)
   stats = t.benchmark(classifier, save=True)
   return stats
   
