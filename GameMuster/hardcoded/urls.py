from django.urls import path
from . import views


app_name='hard'


urlpatterns = [
    path('', views.mainpage, name='mainp'),
    path('info/', views.detailpage, name='info')
]