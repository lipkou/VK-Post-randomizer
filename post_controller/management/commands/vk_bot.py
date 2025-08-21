import os
import time
import pytz
import requests
from post_controller.models.category import Category
from post_controller.models.statick_categories import StatickCategory
from post_controller.models.weekDays import WeekDay
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import models 
import vk_api
import random  
from datetime import datetime, timedelta  
from django.utils import timezone


def restart_categorry(categorry, static=False):
    if static:
        midia_list = categorry.st_media.all()
        for st_media in midia_list:
            st_media.used = False
            st_media.save()
    else:
        media_list = categorry.media.all()
        message_list = categorry.messages.all()
        for media in media_list:
            media.used = False
            media.save()
        
        for message in message_list:
            message.used = False
            message.save()
        
    categorry.last_restarted = timezone.now()
    categorry.save()
        
        
class Command(BaseCommand):
    help = 'Создание отложенных постов на следующую неделю по расписанию категорий'
    def add_arguments(self, parser):
        parser.add_argument('--start', type=str, help='Start date in YYYY-MM-DD format')
        parser.add_argument('--end', type=str, help='End date in YYYY-MM-DD format')

    def handle(self, *args, **kwargs):
        start_str = kwargs['start']
        end_str = kwargs['end']

        moscow_tz = pytz.timezone("Europe/Moscow")

        start_date = datetime.strptime(start_str, "%Y-%m-%d").astimezone(moscow_tz)
        end_date = datetime.strptime(end_str, "%Y-%m-%d").astimezone(moscow_tz)
        print(f"Start: {start_date}, End: {end_date}")
        
        vk_session = vk_api.VkApi(token=settings.VK_TOKEN)
        vk = vk_session.get_api()
        upload = vk_api.VkUpload(vk_session)
        me = vk.users.get()
        group_info = vk.groups.getById(group_id=settings.GROUP_ID)
        # Проходимся по всем дням и загружаем медиа
        analizing_date = start_date
        while analizing_date <= end_date:
            # print(f"{analizing_date}:", analizing_date.weekday())
            
            week_day = WeekDay.objects.get(code=str(analizing_date.weekday() + 1))
            categories = Category.objects.filter(week_days=week_day)
            statick_categories = StatickCategory.objects.filter(week_days=week_day)
            

            ###################
            # Статические категории (категории с привязаным сообщением к ней)
            ###################
            for st_category in statick_categories:
                # Дата и время публикации
                publish_datetime = moscow_tz.localize(datetime.combine(analizing_date, st_category.time))
                publish_timestamp = int(publish_datetime.timestamp())

                # Медиа и сообщение
                media_list = list(st_category.st_media.filter(used=False))
                if not media_list:
                    print("-" * 15)
                    print(f"[{st_category.name}] Нет доступных СТАТИЧЕСКИХ медиа на {analizing_date}")
                    print("Начался рестарт всей информации в категории.")
                    if st_category.last_restarted:
                        delta = timezone.now() - st_category.last_restarted
                        print(f"Последний рестарт был {delta.days} дней назад ({st_category.last_restarted})")
                    print("-" * 15)
                    restart_categorry(st_category, static=True)
                    
                
                media = random.choice(media_list)
                message = media.text
                

                # Собираем все непустые изображения
                image_paths = [
                    getattr(media, f'image{i}').path
                    for i in range(2, 11)
                    if getattr(media, f'image{i}')
                ]
                image_paths.insert(0, media.image.path)

                if not image_paths:
                    print(f"[{st_category.name}] У медиа ID {media.id} нет изображений")
                    continue

                # Загружаем в VK
                attachments = []
                for path in image_paths:
                    try:
                        upload_response = upload.photo_wall(path, group_id=settings.GROUP_ID)
                        photo_id = f'photo{upload_response[0]["owner_id"]}_{upload_response[0]["id"]}'
                        attachments.append(photo_id)
                    except Exception as e:
                        print(f"Ошибка загрузки фото: {e}")

                if not attachments:
                    print(f"[{st_category.name}] Не удалось загрузить изображения")
                    continue

                # Отправка отложенного поста
                try:
                    vk.wall.post(
                        owner_id=-settings.GROUP_ID,
                        from_group=1,
                        message=message,
                        attachments=','.join(attachments),
                        publish_date=publish_timestamp
                    )
                    print(f"[{st_category.name}] Запланирован СТАТИЧЕСКИЙ пост на {publish_datetime}")

                    media.used = True
                    media.used_time = publish_datetime
                    media.save()
                except Exception as e:
                    print(f"Ошибка при публикации поста: {e}")



            ###################
            # Обычные категории (не статические)
            ###################
            for category in categories:
                # Дата и время публикации
                publish_datetime = moscow_tz.localize(datetime.combine(analizing_date, category.time))
                publish_timestamp = int(publish_datetime.timestamp())

                # Рандомные медиа и сообщение
                images_qs = list(category.media.filter(used=False))
                messages_qs = list(category.messages.filter(used=False))

                if not images_qs or not messages_qs:
                    print("-" * 15)
                    print(f"[{category.name}] Нет доступных медиа или сообщений на {analizing_date}")
                    print("Начался рестарт всей информации в категории.")
                    if category.last_restarted:
                        delta = timezone.now() - category.last_restarted
                        print(f"Последний рестарт был {delta.days} дней назад ({category.last_restarted})")
                    print("-" * 15)
                    restart_categorry(category)
                    continue

                media = random.choice(images_qs)
                message = random.choice(messages_qs)

                # Собираем все непустые изображения
                image_paths = [
                    getattr(media, f'image{i}').path
                    for i in range(2, 11)
                    if getattr(media, f'image{i}')
                ]
                image_paths.insert(0, media.image.path)

                if not image_paths:
                    print("-" * 15)
                    print(f"[{category.name}] У медиа ID {media.id} нет изображений")
                    print("Начался рестарт всей информации в категории.")
                    if category.last_restarted:
                        delta = timezone.now() - category.last_restarted
                        print(f"Последний рестарт был {delta.days} дней назад ({category.last_restarted})")
                    print("-" * 15)
                    restart_categorry(category)
                    

                # Загружаем в VK
                attachments = []
                for path in image_paths:
                    try:
                        #################
                        # TODO: Скопировать этот код и вставить в обычную категорию на обработку изображений. 
                        
                        upload_server = vk.photos.getWallUploadServer(group_id=settings.GROUP_ID)

                        
                        # Открываем текущее изображение
                        with open(path, 'rb') as image_file:
                            response = requests.post(upload_server['upload_url'], files={'photo': image_file}).json()
                        
                        save_response = vk.photos.saveWallPhoto(group_id=settings.GROUP_ID, photo=response['photo'], server=response['server'], hash=response['hash'])
                        photo_id = f"photo{save_response[0]['owner_id']}_{save_response[0]['id']}"
                        attachments.append(photo_id)
                        
                        #################
                    except Exception as e:
                        print(f"Ошибка загрузки фото: {e}")

                if not attachments:
                    print(f"[{category.name}] Не удалось загрузить изображения")
                    continue

                # Отправка отложенного поста
                try:
                    vk.wall.post(
                        owner_id=-settings.GROUP_ID,
                        from_group=1,
                        message=message.text + f"\n {category.signature}",
                        attachments=','.join(attachments),
                        publish_date=publish_timestamp
                    )
                    print(f"[{category.name}] Запланирован пост на {publish_datetime}")

                    media.used = True
                    media.used_time = publish_datetime
                    media.save()

                    message.used = True
                    message.used_time = publish_datetime
                    message.save()

                except Exception as e:
                    print(f"Ошибка при публикации поста: {e}")


            
            analizing_date += timedelta(days=1)
            
        print("=" * 15)
        print("Загрузка прошла успешно.")
        print(f"C {start_date};")
        print(f"До {end_date};")
        print("=" * 15)
        
        ''' # Автоматическое пополнение медиа
    
        moscow_tz = pytz.timezone("Europe/Moscow")
        # print(start_date, end_date)
        # Получаем дату следующего понедельника
        today = timezone.now().astimezone(moscow_tz).date()
        days_ahead = (7 - today.weekday()) % 7  # сколько дней до следующего понедельника
        next_monday = today + timedelta(days=days_ahead or 7)

        # Составляем mapping кодов дней недели к датам следующей недели
        weekday_code_to_date = {
            str(i + 1): next_monday + timedelta(days=i) for i in range(7)
        }

        vk_session = vk_api.VkApi(token=settings.VK_TOKEN)
        vk = vk_session.get_api()
        upload = vk_api.VkUpload(vk_session)
        
        ###################
        # Статические категории (категории с привязаным сообщением к ней)
        ###################
        st_categories_list = list(StatickCategory.objects.all())
        for st_category in st_categories_list:
            category_days = [wd.code for wd in st_category.week_days.all()]
            
            for code in category_days:
                post_date = weekday_code_to_date.get(code)
                if not post_date:
                    continue  # Дата не найдена (в теории не должно быть)

                # Дата и время публикации
                publish_datetime = moscow_tz.localize(datetime.combine(post_date, st_category.time))
                publish_timestamp = int(publish_datetime.timestamp())

                # Медиа и сообщение
                media_list = list(st_category.st_media.filter(used=False))
                if not media_list:
                    print(f"[{st_category.name}] Нет доступных медиа на {post_date}")
                    # restart_categorry(st_category, static=True)
                    continue
                
                media = random.choice(media_list)
                message = media.text
                

                # Собираем все непустые изображения
                image_paths = [
                    getattr(media, f'image{i}').path
                    for i in range(2, 11)
                    if getattr(media, f'image{i}')
                ]
                image_paths.insert(0, media.image.path)

                if not image_paths:
                    print(f"[{st_category.name}] У медиа ID {media.id} нет изображений")
                    continue

                # Загружаем в VK
                attachments = []
                for path in image_paths:
                    try:
                        upload_response = upload.photo_wall(path, group_id=settings.GROUP_ID)
                        photo_id = f'photo{upload_response[0]["owner_id"]}_{upload_response[0]["id"]}'
                        attachments.append(photo_id)
                    except Exception as e:
                        print(f"Ошибка загрузки фото: {e}")

                if not attachments:
                    print(f"[{st_category.name}] Не удалось загрузить изображения")
                    continue

                # Отправка отложенного поста
                try:
                    vk.wall.post(
                        owner_id=-settings.GROUP_ID,
                        from_group=1,
                        message=message,
                        attachments=','.join(attachments),
                        publish_date=publish_timestamp
                    )
                    print(f"[{st_category.name}] Запланирован пост на {publish_datetime}")

                    media.used = True
                    media.used_time = publish_datetime
                    media.save()

                except Exception as e:
                    print(f"Ошибка при публикации поста: {e}")

        ###################
        # обычные категории (не статические)
        ###################
        categories_list = list(Category.objects.all())
        for category in categories_list:
            category_days = [wd.code for wd in category.week_days.all()]
            
            for code in category_days:
                post_date = weekday_code_to_date.get(code)
                if not post_date:
                    continue  # Дата не найдена (в теории не должно быть)

                # Дата и время публикации
                publish_datetime = moscow_tz.localize(datetime.combine(post_date, category.time))
                publish_timestamp = int(publish_datetime.timestamp())

                # Рандомные медиа и сообщение
                images_qs = list(category.media.filter(used=False))
                messages_qs = list(category.messages.filter(used=False))

                if not images_qs or not messages_qs:
                    print(f"[{category.name}] Нет доступных медиа или сообщений на {post_date}")
                    restart_categorry(category)
                    continue

                media = random.choice(images_qs)
                message = random.choice(messages_qs)

                # Собираем все непустые изображения
                image_paths = [
                    getattr(media, f'image{i}').path
                    for i in range(2, 11)
                    if getattr(media, f'image{i}')
                ]
                image_paths.insert(0, media.image.path)

                if not image_paths:
                    print(f"[{category.name}] У медиа ID {media.id} нет изображений")
                    restart_categorry(category)
                    continue

                # Загружаем в VK
                attachments = []
                for path in image_paths:
                    try:
                        upload_response = upload.photo_wall(path, group_id=settings.GROUP_ID)
                        photo_id = f'photo{upload_response[0]["owner_id"]}_{upload_response[0]["id"]}'
                        attachments.append(photo_id)
                    except Exception as e:
                        print(f"Ошибка загрузки фото: {e}")

                if not attachments:
                    print(f"[{category.name}] Не удалось загрузить изображения")
                    continue

                # Отправка отложенного поста
                try:
                    vk.wall.post(
                        owner_id=-settings.GROUP_ID,
                        from_group=1,
                        message=message.text + f"\n {category.signature}",
                        attachments=','.join(attachments),
                        publish_date=publish_timestamp
                    )
                    print(f"[{category.name}] Запланирован пост на {publish_datetime}")

                    media.used = True
                    media.used_time = publish_datetime
                    media.save()

                    message.used = True
                    message.used_time = publish_datetime
                    message.save()

                except Exception as e:
                    print(f"Ошибка при публикации поста: {e}")

        '''
        