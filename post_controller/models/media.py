from django.db import models


class Media(models.Model):
    categories = models.ManyToManyField("post_controller.Category", related_name='media')
    image = models.ImageField()
    image2 = models.ImageField()
    image3 = models.ImageField()
    image4 = models.ImageField()
    image5 = models.ImageField()
    image6 = models.ImageField()
    image7 = models.ImageField()
    image8 = models.ImageField()
    image9 = models.ImageField()
    image10 = models.ImageField()
    used = models.BooleanField(default=False)
    
    class Meta:
        verbose_name="Изображение"
        verbose_name_plural="Изображения"

        
    def __str__(self):
        return f"Media ID {self.id}"