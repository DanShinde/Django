from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('video_feed', views.videofeed, name='video_feed'),
    path('create_folder/', views.create_folder, name='create_folder'),
    path('start_photos/', views.start_Photos, name='start_photos'),
    path('record/', views.record_view, name='record'),

    path('/selectfolder', views.selectfolder, name='selectfolder'),

]

