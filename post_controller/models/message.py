from django.db import models


class Message(models.Model):
    categories = models.ManyToManyField("post_controller.Category", related_name='messages')
    text = models.TextField()
    
    class Meta:
        verbose_name="Сообщение"
        verbose_name_plural="Сообщения"

    
    def __str__(self):
        return f"Message: {self.text[:30]}"