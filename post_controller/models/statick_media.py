from django.db import models


class StatickMedia(models.Model):
    categories = models.ManyToManyField("post_controller.StatickCategory", related_name='st_media')
    text = models.TextField()
    image = models.ImageField()
    image2 = models.ImageField(blank=True, null=True)
    image3 = models.ImageField(blank=True, null=True)
    image4 = models.ImageField(blank=True, null=True)
    image5 = models.ImageField(blank=True, null=True)
    image6 = models.ImageField(blank=True, null=True)
    image7 = models.ImageField(blank=True, null=True)
    image8 = models.ImageField(blank=True, null=True)
    image9 = models.ImageField(blank=True, null=True)
    image10 = models.ImageField(blank=True, null=True)
    used = models.BooleanField(default=False)
    used_time = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name="Статическое изображение"
        verbose_name_plural="Статические изображения"

        
    def __str__(self):
        return f"St. Media ID {self.id}"