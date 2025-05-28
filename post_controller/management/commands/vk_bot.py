import os
import time
import pytz
from post_controller.models.category import Category
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import models 
import vk_api
import random  
from datetime import datetime, timedelta  



class Command(BaseCommand):
    help = 'Выводит случайное сообщение и изображение из категории с ID=1'

    def handle(self, *args, **kwargs):
        categories_list = list(Category.objects.all())
        
        # work with vk 
        vk_session = vk_api.VkApi(token=settings.VK_TOKEN)
        vk = vk_session.get_api()
        upload = vk_api.VkUpload(vk_session)
        
        for category in categories_list:
            images = list(category.media.filter(used=False).all())
            messages = list(category.messages.filter(used=False).all())
            # print(images)
            # print(messages)
            
            if not images:
                print("Не найдено картинок")
                continue
            elif not messages:
                print("Не найдено сообщений")
                continue
            
            chosed:list[models.Model] = []
            chosed.append(random.choice(images))
            chosed.append(random.choice(messages))
            
            # load photo or gif in vk
            upload_response = upload.photo_wall(chosed[0].image.path, group_id=settings.GROUP_ID)
            attachment = f'photo{upload_response[0]["owner_id"]}_{upload_response[0]["id"]}'

            # get and transform time
            moscow_tz = pytz.timezone("Europe/Moscow")
            category_time = category.time
            
            tomorrow = datetime.now(moscow_tz).date() + timedelta(days=1)
            combined_datetime = datetime.combine(tomorrow, category_time)
            localized = moscow_tz.localize(combined_datetime)
            publish_timestamp = int(localized.timestamp())
            
            # sending post
            vk.wall.post(
                owner_id=-settings.GROUP_ID,  # with "-" ID group
                from_group=1,
                message=chosed[1].text,
                attachments=attachment,
                publish_date=publish_timestamp
            )
            

            print("Опубликирован пост:", chosed)
            
            for model in chosed: 
                model.used = True 
                model.save()
            
            # print(list(category.messages.filter(used=False).all()))
            time.sleep(10)
                