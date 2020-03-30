from django.urls import path

from . import views

app_name = 'edge'
urlpatterns = [
    path('', views.index, name='index'),
    path('save', views.save, name='save'),
    path('visualize', views.visualize, name='visualize'),
    path('create_links', views.create_links, name='create_links')
]