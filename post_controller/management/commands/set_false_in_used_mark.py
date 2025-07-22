import os
import time
import pytz
from post_controller.models.media import Media
from post_controller.models.message import Message
from post_controller.models.statick_media import StatickMedia
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import models 
import vk_api
import random  
from datetime import datetime, timedelta  
from django.utils import timezone



class Command(BaseCommand):
    help = 'Указывает что всё (абсолютно всё) не использовалось раньше'

    def handle(self, *args, **kwargs):
        media_list = Media.objects.all()
        message_list = Message.objects.all()
        st_media_list = StatickMedia.objects.all()
        
        for media in media_list:
            media.used = False
            media.save()
        
        for message in message_list:
            message.used = False
            message.save()
        
        for st_media in st_media_list:
            st_media.used = False
            st_media.save()
        print("Done")