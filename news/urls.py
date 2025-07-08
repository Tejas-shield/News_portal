from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detail/', views.article_detail, name='detail'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('send-telegram/', views.trigger_telegram_news, name='send_telegram_news'),
]
