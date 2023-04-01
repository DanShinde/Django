
from django.urls import path

from . import views

urlpatterns = [
    path('', views.folder_list, name='folder_list'),
    path('<str:folder_name>/', views.folder_detail, name='folder_detail'),
]