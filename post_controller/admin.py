from django.contrib import admin
from post_controller.forms import MediaAdminForm
from post_controller.models.category import Category
from post_controller.models.media import Media
from post_controller.models.message import Message
from post_controller.models.statick_categories import StatickCategory
from post_controller.models.statick_categories import WeekDay
from post_controller.models.statick_media import StatickMedia
from django.utils.html import mark_safe



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', "signature", 'time', "day_list", "media_count", "message_count", "last_restarted"]
    
    def media_count(self, obj):
        return obj.media.count()
    media_count.short_description = "Изображений"

    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = "Сообщений"

    def day_list(self, obj):
        return ", ".join(c.name for c in obj.week_days.all())
    day_list.short_description = "Дни отправки"
    
@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    form = MediaAdminForm
    list_display = ['id', 'preview', 'categories_list', "used_time", "used"]
    list_display_links = ['id', 'preview']
    filter_horizontal = ['categories']
    
    list_filter = ['categories']  

    def categories_list(self, obj):
        return ", ".join(c.name for c in obj.categories.all())
    categories_list.short_description = 'Категории'

    def preview(self, obj):
        html = ""
        for i in range(1, 11):
            image_field = getattr(obj, f'image{i if i > 1 else ""}', None)
            if image_field:
                html += f'<img src="{image_field.url}" width="100" style="margin: 2px; object-fit: contain;" />'
        return mark_safe(html or 'Нет изображений')
    preview.short_description = 'Превью'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'short_text', 'categories_list', "used_time", "used",]
    list_display_links = ['id', 'short_text', ]
    filter_horizontal = ['categories']
    
    list_filter = ['categories']
     
    def short_text(self, obj):
        return obj.text[:50]
    short_text.short_description = 'Text'

    def categories_list(self, obj):
        return ", ".join(c.name for c in obj.categories.all())
    categories_list.short_description = 'Категории'


@admin.register(StatickCategory)
class StCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "signature", "media_count", "time", "day_list", "last_restarted", ]
    def media_count(self, obj):
        return obj.st_media.count()
    media_count.short_description = "Ст. Медия"
    
    def day_list(self, obj):
        return ", ".join(c.name for c in obj.week_days.all())
    day_list.short_description = "Дни отправки"


@admin.register(StatickMedia)
class StMediaAdmin(admin.ModelAdmin):
    form = MediaAdminForm
    list_display = ['id', 'preview', 'categories_list', "used_time", "used",]
    list_display_links = ['id', 'preview', ]
    filter_horizontal = ['categories']  
    
    list_filter = ['categories'] 
    
    def categories_list(self, obj):
        return ", ".join(c.name for c in obj.categories.all())
    categories_list.short_description = 'Категории'
    
    def preview(self, obj):
        html = ""
        for i in range(1, 11):
            image_field = getattr(obj, f'image{i if i > 1 else ""}', None)
            if image_field:
                html += f'<img src="{image_field.url}" width="100" style="margin: 2px; object-fit: contain;" />'
        return mark_safe(html or 'Нет изображений')
    preview.short_description = 'Превью'
    
@admin.register(WeekDay)
class WeekDayAdmin(admin.ModelAdmin):
    pass
    