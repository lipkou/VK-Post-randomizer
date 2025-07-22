from django.db import models
from post_controller.models.weekDays import WeekDay



class StatickCategory(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    week_days = models.ManyToManyField(WeekDay, verbose_name="Дни недели")
    time = models.TimeField()
    last_restarted = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name="Статичиская категория"
        verbose_name_plural="Статические категории"

    def __str__(self):
        st_media = self.st_media.count()
        return f'{self.name} (Медиа: {st_media});'
