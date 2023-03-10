from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('video_feed', views.videofeed, name='video_feed'),
    path('create_folder', views.create_folder, name='create_folder'),
    path('start_Photos', views.start_Photos, name='start_Photos'),
    # path('browser', views.browse_folder, name='browse_folder'),
    # path('StoredData/<path:path>', views.view_media, name='view_media'),
    # path('take_video', views.take_Video, name='take_Video'),
    # path('video_feed', views.video_feed, name='video_feed'),
    # path('start_stream', views.start_stream, name='start_stream'),
    # path('stop_stream', views.stop_stream, name='stop_stream'),
    # path('rec_on', views.rec_on, name='rec_on'),
    # path('rec_off', views.rec_off, name='rec_off'),
]
