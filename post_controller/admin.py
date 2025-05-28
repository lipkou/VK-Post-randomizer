from django.contrib import admin
from post_controller.forms import MediaAdminForm
from post_controller.models.category import Category
from post_controller.models.media import Media
from post_controller.models.message import Message
from django.utils.html import mark_safe



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'time', "media_count", "message_count"]
    
    def media_count(self, obj):
        return obj.media.count()
    media_count.short_description = "Изображений"

    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = "Сообщений"
    
@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    form = MediaAdminForm
    list_display = ['id', 'preview', 'categories_list', "used",]
    filter_horizontal = ['categories']  
    list_display_links = ['id', 'preview', ]
    
    def categories_list(self, obj):
        return ", ".join(c.name for c in obj.categories.all())
    categories_list.short_description = 'Категории'
    
    def preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" style="object-fit: contain;" />')
        return 'Нет изображения'
    preview.short_description = 'Превью'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'short_text', 'categories_list', "used",]
    filter_horizontal = ['categories']
    list_display_links = ['id', 'short_text', ]
    
    def short_text(self, obj):
        return obj.text[:50]
    short_text.short_description = 'Text'

    def categories_list(self, obj):
        return ", ".join(c.name for c in obj.categories.all())
    categories_list.short_description = 'Категории'
    
    