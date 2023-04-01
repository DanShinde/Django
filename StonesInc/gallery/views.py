import os
from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from main.views import stop_cam

stored_data_dir = os.path.join(settings.MEDIA_ROOT, 'StoredData')

def folder_list(request):
    folders = os.listdir(stored_data_dir)
    stop_cam()
    return render(request, 'gallery/folder_list.html', {'folders': folders})


def folder_detail(request, folder_name):
    folder_path = os.path.join(stored_data_dir, folder_name)
    storage = FileSystemStorage(location=folder_path)
    files = storage.listdir(folder_path)[1]
    jpg_files = []
    mp4_files = []
    for filename in files:
        name, ext = os.path.splitext(filename)
        if ext == '.jpg':
            jpg_files.append(os.path.join('\\media\\StoredData', folder_name, filename))
        elif ext == '.mp4':
            mp4_files.append(os.path.join('/StoredData', folder_name, filename))
    return render(request, 'gallery/folder_detail.html', {'folder_name': folder_name, 'jpg_files': jpg_files, 'mp4_files': mp4_files})
