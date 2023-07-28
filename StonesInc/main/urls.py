from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.Home, name='home'),
    path('stream/', views.stream_video, name='stream_video'),
    # path('video_feed', views.videofeed, name='video_feed'),
    path('create_folder/', views.create_folder, name='create_folder'),
    path('start_photos/', views.start_Photos, name='start_photos'),
    path('record/', views.record_view, name='record'),
    path('update_zoom_factor/', views.update_zoom_factor, name='update_zoom_factor'),
    path('update_camera_controls/', views.update_camera_controls, name='update_camera_controls'),
    
    path('selectfolder/<str:folder>/', views.selectfolder, name='selectfolder'),
    path('redirect_to_Gallery', views.redirect_to_Gallery, name='redirect_to_Gallery'),


]

