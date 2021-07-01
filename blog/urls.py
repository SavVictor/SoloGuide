from django.urls import path
from . import views
from .views import CustomLoginView, RegisterPage, GuideCreate, GuideUpdate, GuideDelete, DetailView, GuideReview
from django.contrib.auth.views import LogoutView
app_name = 'blog'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='blog:home'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('guide-create/', GuideCreate.as_view(), name='guide-create'),
    path('guide-review/', GuideReview.as_view(), name='guide-review'),

    path('', views.home, name='home'),
    path('articles/', views.articles, name='articles'),
    path('<slug:article>/', views.article, name='article'),
    path('<slug:slug>/guide-update/', GuideUpdate.as_view(), name='guide-update'),
    path('<slug:slug>/guide-delete/', GuideDelete.as_view(), name='guide-delete'),
]
