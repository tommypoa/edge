from django.urls import path

from . import views

app_name = 'edge'
urlpatterns = [
    path('', views.select_island, name='select_island'),
    path('merge/<str:island>', views.index, name='index'),
    path('save', views.save, name='save'),
    path('visualize', views.visualize, name='visualize'),
    path('create_links', views.create_links, name='create_links'),
    path('create_duplicates', views.create_duplicates, name='create_duplicates'),
    path('change_island_name', views.change_island_name, name='change_island_name')
]