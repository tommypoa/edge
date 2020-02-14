from django.urls import path

from . import views

app_name = 'edge'
urlpatterns = [
    path('', views.index, name='index'),
    path('save', views.save, name='save')
]