from django import forms
from post_controller.models.category import Category
from post_controller.models.media import Media
from post_controller.models.message import Message
from django import forms
from django.utils.safestring import mark_safe

class MediaAdminForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            for i in range(1, 11):
                field_name = f'image{i}' if i > 1 else 'image'
                image_field = getattr(self.instance, field_name, None)

                if image_field:
                    self.fields[field_name].help_text = mark_safe(
                        f'<a href="{image_field.url}" target="_blank">'
                        f'<img src="{image_field.url}" width="200" '
                        f'style="margin-top:10px; max-height:200px; object-fit:contain;" />'
                        f'</a>'
                    )

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

