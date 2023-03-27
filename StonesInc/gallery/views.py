import os
from django.conf import settings
from django.shortcuts import render

def get_gallery_items():
    # Get the path to the StoredData directory
    stored_data_dir = os.path.join(settings.MEDIA_ROOT, 'StoredData')

    # Traverse the directory and generate a list of gallery items
    gallery_items = []
    for root, dirs, files in os.walk(stored_data_dir):
        # Add the directories as gallery items
        for directory in dirs:
            directory_path = os.path.join(root, directory)
            thumbnail = get_first_image_path(directory_path)
            gallery_items.append({'type': 'folder', 'name': directory, 'thumbnail': thumbnail})

        # Add the images and videos as gallery items
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
                gallery_items.append({'type': 'image', 'name': file, 'thumbnail': file})
            elif file_extension in ['.mp4', '.webm', '.ogg']:
                gallery_items.append({'type': 'video', 'name': file, 'thumbnail': get_video_thumbnail_path(file_path)})

    return gallery_items

def get_first_image_path(directory_path):
    # Get the path to the first image file in the directory
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
                return file_path
    # If no image file is found, return a default thumbnail
    return 'default-folder-thumbnail.jpg'

def get_video_thumbnail_path(video_path):
    # Use ffmpeg to generate a thumbnail image for the video
    thumbnail_path = os.path.splitext(video_path)[0] + '.jpg'
    if not os.path.isfile(thumbnail_path):
        os.system(f'ffmpeg -i {video_path} -ss 00:00:01.000 -vframes 1 {thumbnail_path}')
    return thumbnail_path

def gallery(request):
    # Get the list of gallery items
    gallery_items = get_gallery_items()

    # Group gallery items by folder (folders are assumed to come before images and videos)
    folders = []
    current_folder = None
    for item in gallery_items:
        if item['type'] == 'folder':
            if current_folder is not None:
                folders.append(current_folder)
            current_folder = {'name': item['name'], 'items': []}
        else:
            current_folder['items'].append({'type': item['type'], 'name': item['name'], 'thumbnail': item['thumbnail']})
    if current_folder is not None:
        folders.append(current_folder)

    # Render the gallery template with the folders and images/videos
    return render(request, 'gallery.html', {'folders': folders})
