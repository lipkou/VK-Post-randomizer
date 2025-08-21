from django.db import models


class WeekDay(models.Model):
    code = models.CharField(max_length=1, unique=True)
    name = models.CharField(max_length=15)
    
    class Meta:
        ordering = ["code"]
        
    def __str__(self):
        return self.name