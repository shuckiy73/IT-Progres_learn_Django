from django.urls import path
from . import views


urlpatterns = [
    path('1', views.url1),
    path('2', views.url2),
    path('3', views.url3),
    path('4', views.url4),
    path('5', views.url5)

]
