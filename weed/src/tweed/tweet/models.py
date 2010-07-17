from django.db import models

class Status(models.Model):
    text = models.CharField(max_length=200, blank=True)
    id = models.IntegerField(primary_key=True)
    
    def __unicode__(self):
        return self.id
    
    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "statuses"
        
