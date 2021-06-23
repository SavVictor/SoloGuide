from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('news/', views.news, name='news'),
    path('articles/', views.articles, name='articles'),
    path('<slug:article>/', views.article, name='article'),
]
