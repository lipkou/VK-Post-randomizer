from django.db import models
from datetime import timedelta
from post_controller.models.weekDays import WeekDay


class Category(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    signature = models.TextField('Подпись', max_length=100, blank=True, null=True)
    week_days = models.ManyToManyField(WeekDay, verbose_name="Дни недели")
    time = models.TimeField(null=False)
    last_restarted = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name="Категория"
        verbose_name_plural="Категории"
    
    def __str__(self):
        media_count = self.media.count()
        message_count = self.messages.count()
        return f'{self.name} (Изображений: {media_count}; Сообщений: {message_count})'

