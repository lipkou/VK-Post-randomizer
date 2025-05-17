from django.db import models


class Media(models.Model):
    categories = models.ManyToManyField("post_controller.Category", related_name='media')
    image = models.ImageField()
    
    class Meta:
        verbose_name="Изображение"
        verbose_name_plural="Изображения"

        
    def __str__(self):
        return f"Media ID {self.id}"