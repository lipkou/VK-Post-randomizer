from django.db import models
from datetime import timedelta


class Category(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    time = models.TimeField(null=False)
    
    class Meta:
        verbose_name="Категория"
        verbose_name_plural="Категории"
    
    def __str__(self):
        media_count = self.media.count()
        message_count = self.messages.count()
        return f'{self.name} (Изображений: {media_count}; Сообщений: {message_count})'