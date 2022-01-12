from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsView.as_view()),
    path('<int:news_id>/', views.SingleNewsView.as_view()),
]
