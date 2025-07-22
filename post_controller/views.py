import os
import subprocess
import sys
import io
from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.utils import timezone
from django.shortcuts import render
from django.core.management import call_command
from .forms import DateRangeForm


def load_media_by_range(request:HttpRequest):
    if request.method == "POST":
        print("Post")
        form = DateRangeForm(request.POST)
        if form.is_valid():
            print("Data:", form.data)
            start_date = form.data["start_date"]
            end_date = form.data["end_date"]
            print(start_date)
            print(end_date)
            
            script_path = os.path.join(settings.BASE_DIR, 'manage.py')
            if sys.platform == 'win32':
                venv_python = os.path.join(settings.BASE_DIR, '.venv', 'Scripts', 'python.exe')
            else:
                venv_python = os.path.join(settings.BASE_DIR, '.venv', 'bin', 'python')

            subprocess.Popen([
                venv_python,
                script_path,
                'vk_bot',
                f'--start={start_date}',
                f'--end={end_date}'
            ])
            
            html_text = f'''
<h2>Скрипт запущен в фоне. Можете продолжать работу.</h2> 
<p>Скрипт заполнит медиа с <b>{start_date}</b> до <b>{end_date}</b>.</p>
'''
            return HttpResponse(html_text)

    else:
        form = DateRangeForm()
        
    return render(request, 'load_media_by_range.html', {'form': form, "now": timezone.now()})