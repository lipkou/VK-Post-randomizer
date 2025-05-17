from django import forms
from post_controller.models.category import Category
from post_controller.models.media import Media
from post_controller.models.message import Message
from django.utils.html import mark_safe


class MediaAdminForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.image:
            self.fields['image'].help_text = mark_safe(
                f'<a href="{self.instance.image.url}"><img src="{self.instance.image.url}" width="200" style="margin-top:10px; max-height:200px; object-fit:contain;" /></a>'
            )
