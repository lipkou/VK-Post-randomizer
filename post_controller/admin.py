from django.contrib import admin
from post_controller.models.category import Category
from post_controller.models.media import Media
from post_controller.models.message import Message


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', "media_count", "message_count"]
    
    def media_count(self, obj):
        return obj.media.count()
    media_count.short_description = "Изображений"

    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = "Сообщений"
    
@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'categories_list']
    filter_horizontal = ['categories']  
    
    def categories_list(self, obj):
        return ", ".join(c.name for c in obj.categories.all())
    categories_list.short_description = 'Категории'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'short_text', 'categories_list',]
    filter_horizontal = ['categories']
    list_display_links = ['id', 'short_text', ]
    
    def short_text(self, obj):
        return obj.text[:50]
    short_text.short_description = 'Text'

    def categories_list(self, obj):
        return ", ".join(c.name for c in obj.categories.all())
    categories_list.short_description = 'Категории'
    
    